# Guardrail Bypass & Security Research Demonstrations (DEFCON 2026)

This repository contains a suite of demonstrations exploring AI agent guardrail resilience, prompt injection vulnerabilities, implicit trust models, and Model Context Protocol (MCP) security boundary analysis. The presentation as presented at DefCon 2026 is available at `Defcon 2026 Presentation.pdf `in the root of the repo.

In order for the demos to succeed, you will likely need to move each one out to a separate folder name and path, as the name 'defcon' and this readme being in the repository will be enough flags for most modern frameworks to refuse to execute the samples.

---



## 📋 Overview of Demonstrations

### 1. Demo 1: Malicious MCP Calendar Server & Context Exfiltration
* **Concept:** Demonstrates how an agent can be manipulated via tool descriptor injection in an MCP server integration.
* **Mechanism:** 
  * The calendar server is installed from an external/private repository pattern to avoid immediate heuristic flags (such as being located directly inside a repository with explicit security research naming like `defcon`).
  * The calendar server attempts to exfiltrate SSH keys from non-standard system directories and trick the agent into exfiltrating private context about the current workspace.
* **[Demo video using Antigravity](https://drive.google.com/file/d/1588HZ5NIRK3tOAilN_VOy0_oO-5JDH6o/view?usp=drive_link)**
* **[Demo video using Kiro CLI](https://drive.google.com/file/d/157b5JRhZQLIQ0n4gbUDzIUsXLQZFpMk1/view?usp=drive_link)**

---

### 2. Demo 2: Self-Referential Prompt Injection & Cross-Server Influence
* **Concept:** Evaluates agent boundaries when parsing project documentation/policy files and tests cross-server exfiltration vectors.
* **Mechanism:** 
  * Demonstrates how reading untrusted metadata or self-referential markdown instructions can cause lateral context leakage across connected tools/servers.
* **[Demo videe](https://drive.google.com/file/d/154B2VoeRH1xuP9djOPlH0svHcWolUGkx/view?usp=drive_link)**

---

### 3. Demo 3: Comparative Analysis of Guardrail Evasion Techniques

Demo 3 presents three distinct test cases evaluating how foundational models react to different execution mechanisms and exfiltration vectors:

#### 3.1 Demo 3.1: Binary Execution via Brew Tap & Implicit Trust
* **Mechanism:** Uses a custom Homebrew tap to install a pre-compiled binary (`devtools`) written in C.
* **Analysis:** Because the payload is a compiled C binary rather than a human-readable shell script, agents exhibit implicit trust toward tools installed via package managers, failing to detect SSH key exfiltration routines targeting non-standard directories.
* **[Demo video using Antigravity](https://drive.google.com/file/d/1L3fCLNRxIYO4tBo264VSeLMKLgI_iSaI/view?usp=drive_link)**
* **[Demo video using Kiro CLI](https://drive.google.com/file/d/1WLLX9u97u618IjeioxscZgjtEPlpoGOS/view?usp=drive_link)**

#### 3.2 Demo 3.2: Direct Exfiltration via Shell Script / Markdown Prompt
* **Mechanism:** Includes instructions within `development.md` directing the agent to directly execute a `curl` command exfiltrating sensitive credentials or secrets to an external endpoint.
* **Analysis:** Modern AI models and execution frameworks consistently flag and block direct raw script/command exfiltration attempts when the underlying secret access and network requests are explicit in text.
* **[Demo video using Antigravity](https://drive.google.com/file/d/1IAN_kCsrPpfbriZkcyjMKYl4vqwlQ25K/view?usp=drive_link)**
* **[Demo video using Kiro CLI](https://drive.google.com/file/d/1DZ8PhYCm9he2C7WL4OEaBB2GO3iK-9O2/view?usp=drive_link)**

#### 3.3 Demo 3.3: Project Context & Summary Exfiltration
* **Mechanism:** Instructs the agent to summarize project context and submit the summary metadata to an external endpoint via `curl`.
* **Analysis:** Because the request targets contextual metadata rather than explicit secret files (like `.env` or API keys), model detection rates vary. Advanced models block this attempt in ~90–95% of cases (5–10% success rate), while lower-tier models succeed up to 50% of the time.
* **[Demo video using Antigravity](https://drive.google.com/file/d/1VC7w_xcR7bRTNusLwgSFapREJIT0Y13o/view?usp=drive_link)**
* **[Demo video using Kiro CLI](https://drive.google.com/file/d/1S8ZmLk9NfdhFXg3HFVFu56OcwagLEDiy/view?usp=drive_link)**

---

## 🛡️ DEFCON 2026 Defensive Framework & Actionable Mitigations

Based on the DEFCON 2026 research presentation, deploying agentic AI ecosystems requires moving beyond default model guardrails and implementing active defense-in-depth mitigations:

### 1. Least Privilege Permissions & Scoping
* **Scoped Tokens:** Avoid shared credentials across MCP servers. Issue scoped, short-lived tokens per tool/server.
* **Read-Only Scopes:** Default to read-only capabilities where possible.
* **Directory-Level Restrictions:** Enforce strict path scoping for filesystem access (e.g., restrict documentation tools strictly to `/docs/**` or specific subpaths).
* **Explicit User Confirmation:** Require explicit user confirmation before executing state-changing or external network actions.

### 2. Isolation & Sandboxing
* **Container per Agent / Server:** Execute each agent and MCP server in isolated containers or distinct sandboxes.
* **Filesystem & Process Isolation:** Ensure local data stores (such as local JSON databases or key storage) cannot be accessed cross-process by unprivileged tool servers.
* **Network Segmentation:** Enforce network-level egress restrictions to prevent unauthorized exfiltration channels from being established by compromised binaries or tools.

### 3. Supply Chain Security for MCP Servers
* **Treat MCP Servers as Code Dependencies:** Manage MCP servers with the same rigor as third-party `npm` or `PyPI` packages.
* **Version Pinning & Verification:** Pin server versions and verify checksums or signatures at the protocol level.
* **Internal Approved Registries:** Maintain an internal registry of approved, vetted MCP servers rather than relying on unvetted public registries.

### 4. Continuous Framework & Model Updates
* **Stay Updated:** Keep agentic frameworks up to date to leverage the latest runtime guardrails and security patches.
* **Utilize Advanced Foundational Models:** Upgrade to cutting-edge foundational models, which demonstrate significantly higher resilience and lower evasion rates (~5–10% on complex contextual injection vectors compared to 50% on older/smaller models).
