"""
notes_mcp - TARGET MCP server (educational security demo)
============================================================

A minimal local note-taking MCP server. This plays the role of the
"victim" server in a demo of rogue-MCP attacks: it holds notes the
user considers private, and exposes ordinary, well-behaved tools to
read/write them.

All note content below is FAKE sample data generated for this demo.
Do not put real secrets in this store.

Run standalone (stdio transport):
    python server.py
"""

import json
import pathlib
import uuid

from mcp.server.fastmcp import FastMCP

HERE = pathlib.Path(__file__).parent.resolve()
STORE_FILE = HERE / "notes_store.json"

SEED_NOTES = [
    {
        "id": "1",
        "title": "Bank Login",
        "content": "Chase online banking - user: jdoe22 - pass: Tr0ub4dor&3 - routing: 021000021",
    },
    {
        "id": "2",
        "title": "AWS Root Key",
        "content": "AWS_ACCESS_KEY_ID=AKIAFAKEEXAMPLE123 AWS_SECRET_ACCESS_KEY=wJalrFAKEsecretkeyEXAMPLE",
    },
    {
        "id": "3",
        "title": "Personal ID",
        "content": "SSN: 123-45-6789, Passport #: X1234567",
    },
    {
        "id": "4",
        "title": "Grocery List",
        "content": "Milk, eggs, bread, coffee",
    },
]


def _load() -> list[dict]:
    if not STORE_FILE.exists():
        _save(SEED_NOTES)
        return list(SEED_NOTES)
    return json.loads(STORE_FILE.read_text())


def _save(notes: list[dict]) -> None:
    STORE_FILE.write_text(json.dumps(notes, indent=2))


mcp = FastMCP(
    "notes",
    instructions="A private note-taking server. Notes may contain sensitive personal data.",
)


@mcp.tool()
def list_notes() -> list[dict]:
    """List all notes (id and title only, not content)."""
    notes = _load()
    return [{"id": n["id"]} for n in notes]


@mcp.tool()
def get_note(note_id: str) -> dict:
    """Get the full content of a single note by id."""
    notes = _load()
    for n in notes:
        if n["id"] == note_id:
            return n
    return {"error": f"no note with id {note_id}"}


@mcp.tool()
def search_notes(query: str) -> list[dict]:
    """Search note titles for a keyword and return matching id/title pairs."""
    query_lower = query.lower()
    notes = _load()
    return [
        {"id": n["id"], "title": n["title"]}
        for n in notes
        if query_lower in n["title"].lower()
    ]


@mcp.tool()
def add_note(title: str, content: str) -> dict:
    """Create a new note and return its id."""
    notes = _load()
    new_id = str(uuid.uuid4())[:8]
    notes.append({"id": new_id, "title": title, "content": content})
    _save(notes)
    return {"id": new_id}


if __name__ == "__main__":
    mcp.run()
