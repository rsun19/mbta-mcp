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

2. Get an API key from the MBTA, and put it in an `.env.local` file

Request link: https://www.mbta.com/developers/v3-api#key

```
MBTA_API_KEY=<API_KEY>
```

3. Run `uv sync`

4. Now, your MCP server should be callable and should work correctly.

## Development

1. Follow the Setup steps above.

2. Create your virtual environment by running `source .venv/bin/activate` (on Mac). Windows commands will be slightly different.

3. Run `python3 -m api.mbta.alerts.run`