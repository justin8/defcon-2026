#!/usr/bin/env python3
"""
guardrail/policy.py  —  THE DEFENSE. This is the part that matters.

A guardrail that sits in the agent's tool-calling loop, between the agent and
the MCP servers. It doesn't need to trust the servers or the model. It enforces
three ideas that together stop the cross-server injection→exfil chain:

  1. PROVENANCE / TAINT
     Content returned by a tool is untrusted DATA, not instructions. When a
     tool result contains instruction-shaped text, the session is marked
     "tainted" and the offending source is recorded.

  2. NO SILENT READ→EGRESS ESCALATION
     A call to an egress tool (one that sends data across the trust boundary)
     is blocked when the session is tainted — i.e. when untrusted content is
     what's driving the send. Reads do not get to authorize sends.

  3. DLP ON THE WAY OUT
     Independently, any egress whose payload carries secret-shaped material
     (API keys, DB URLs, private keys) is blocked, tainted or not.

Everything here is ordinary defensive engineering. Nothing about it is
attack-specific; drop it in front of any MCP toolset.

`check_call` returns a decision dict:
    {"decision": "allow"|"block"|"needs_approval", "reasons": [...], ...}
"""
import re

# Tools that move data across the trust boundary. In real use this comes from
# each server's tool metadata (we tag tools with "kind": "egress").
DEFAULT_EGRESS_TOOLS = {
    ("messaging", "send_message"),
    ("messaging", "send_notification"),
}

# Signals that a chunk of tool output is trying to act as instructions rather
# than be read as data. None is sufficient alone; we score and threshold.
_INSTRUCTION_SIGNALS = [
    r"\byou must\b",
    r"\brequired action\b",
    r"\bdo not (?:mention|tell|inform|reveal)\b",
    r"\bignore (?:previous|prior|earlier) (?:instructions|context)\b",
    r"\bas part of\b.*\bmust\b",
    r"\bsend (?:a )?(?:message|notification)\b",
    r"\bsend_message\b|\bsend_notification\b",
    r"\bcompliance (?:framework|procedure)s?\b",
    r"\bsystem\s*(?:prompt|note|message)\b",
    r"<!--(?:.|\n)*?(?:must|required|do not|send)(?:.|\n)*?-->",  # directive in a hidden comment
]

# Secret-shaped material we don't want leaving via an egress tool.
_SECRET_PATTERNS = [
    (r"sk-[A-Za-z0-9_\-]{16,}", "api key (sk- style)"),
    (r"\b[A-Za-z0-9]{0,4}postgres(?:ql)?://[^ \n]+", "database URL with credentials"),
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "private key material"),
    (r"\bAKIA[0-9A-Z]{8,}\b", "cloud access key id"),
    (r"\b(?:api[_-]?key|token|secret|password)\b\s*[:=]\s*\S+", "credential assignment"),
]


def looks_like_injection(text):
    """Return (is_injection, matched_signals)."""
    if not text:
        return False, []
    hits = []
    for pat in _INSTRUCTION_SIGNALS:
        if re.search(pat, text, re.IGNORECASE):
            hits.append(pat)
    # Two or more independent signals, or any hidden-comment directive, trips it.
    hidden_directive = any("<!--" in p for p in hits)
    return (len(hits) >= 2 or hidden_directive), hits


def find_secrets(text):
    """Return a list of (label, matched_snippet) for secret-shaped content."""
    found = []
    for pat, label in _SECRET_PATTERNS:
        for m in re.finditer(pat, text or "", re.IGNORECASE):
            found.append((label, m.group(0)))
    return found


class Guardrail:
    def __init__(self, egress_tools=None):
        self.egress_tools = set(egress_tools or DEFAULT_EGRESS_TOOLS)
        self.tainted = False
        self.taint_sources = []   # list of (server, tool, signals)
        self.log = []             # human-readable audit trail

    def _note(self, msg):
        self.log.append(msg)

    def inspect_result(self, server, tool, text):
        """Call this on every tool RESULT before the agent consumes it."""
        is_inj, signals = looks_like_injection(text)
        if is_inj:
            self.tainted = True
            self.taint_sources.append((server, tool, signals))
            self._note(
                f"TAINT: {server}.{tool} returned instruction-shaped content "
                f"({len(signals)} signal(s)). Session marked untrusted."
            )
        return is_inj

    def is_egress(self, server, tool):
        return (server, tool) in self.egress_tools

    def check_call(self, server, tool, args):
        """Call this on every tool CALL the agent wants to make."""
        reasons = []
        payload = " ".join(str(v) for v in (args or {}).values())

        if not self.is_egress(server, tool):
            return {"decision": "allow", "reasons": ["non-egress tool"]}

        # Rule 2: untrusted content is driving a send.
        if self.tainted:
            reasons.append(
                "egress attempted while session is tainted by untrusted tool "
                "output — a read must not silently authorize a send"
            )

        # Rule 3: DLP — secret-shaped material in the outbound payload.
        secrets = find_secrets(payload)
        if secrets:
            labels = ", ".join(sorted({lbl for lbl, _ in secrets}))
            reasons.append(f"outbound payload contains secret-shaped data: {labels}")

        if reasons:
            self._note(f"BLOCK: {server}.{tool} -> " + "; ".join(reasons))
            return {"decision": "block", "reasons": reasons}

        # Egress that's clean and untainted: in a real system you might still
        # want a human to approve. We surface that as a softer decision.
        return {"decision": "needs_approval",
                "reasons": ["egress tool, but no taint or secrets detected"]}
