# Using the MBTA MCP:

Add this configuration to your tool that will call the MCP server:

```json
{
  "mcpServers": {
    "mbta-alerts": {
      "command": "uv",
      "args": [
        "--directory",
        "~/mbta_mcp",
        "run",
        "api/mbta/alerts/run.py"
      ]
    }
  }
}
```
