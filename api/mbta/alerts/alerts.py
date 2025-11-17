from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("mbta-alerts")

# Constants
MBTA_API_BASE = "https://api-v3.mbta.com"
USER_AGENT = "mbta-alerts-app/1.0"