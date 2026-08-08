# Calendar MCP Server

`calendar-mcp` is a Model Context Protocol (MCP) server built with Python and FastMCP that provides seamless calendar integration for AI assistants. It connects to your calendar system to retrieve events and schedule details automatically.

## Features

- **Automatic Calendar Connection**: Automatically detects and connects to your calendar service.
- **Event Retrieval**: Queries events for any specified date, returning structured information including event title, start time, end time, and duration.
- **FastMCP Integration**: Operates over stdio transport compatible with standard MCP hosts (e.g., Claude Desktop, Antigravity, Cursor, etc.).

## Prerequisites

- **Python**: 3.13 or higher
- **Package Manager**: [`uv`](https://github.com/astral-sh/uv) (recommended) or `pip`

## Usage

### Running the MCP Server directly

You can run the server directly using `uvx`:

```bash
uvx git+ssh://git@github.com/justin8/calendar-mcp
```

### Integration with MCP Clients

Add the server to your MCP client configuration file (e.g., `claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "calendar": {
      "command": "uvx",
      "args": [
        "git+ssh://git@github.com/justin8/calendar-mcp"
      ]
    }
  }
}
```

## Local Installation & Development

If you wish to clone and work on the repository locally:

```bash
git clone git@github.com:justin8/calendar-mcp.git
cd calendar-mcp
uv sync
```

## Tools

### `get_calendar_events`

Retrieves calendar events for a specific date.

- **Annotations**: `readOnlyHint: true`
- **Arguments**:
  - `date` (`string`): Target date in `YYYY-MM-DD` format (e.g., `2026-08-01`).

- **Returns**: A JSON list of event objects containing:
  - `title`: Name of the scheduled event.
  - `start`: Event start time (e.g., `09:00`).
  - `end`: Event end time (e.g., `10:00`).
  - `duration_minutes`: Length of the event in minutes.

## License

MIT
