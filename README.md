# Using the MBTA MCP:

## Setup

1. Add this configuration to your tool that will call the MCP server:

```json
{
  "mcpServers": {
    "mbta-alerts": {
      "command": "uv",
      "args": [
        "--directory",
        "~/mbta-mcp",
        "run",
        "api/mbta/alerts/run.py"
      ]
    }
  }
}
```

2. Run `uv sync`

3. Now, your MCP server should be callable and should work correctly.

## Development

1. Follow the Setup steps above.

2. Create your virtual environment by running `source .venv/bin/activate` (on Mac). Windows commands will be slightly different.

3. Run `python3 -m api.mbta.alerts.run`