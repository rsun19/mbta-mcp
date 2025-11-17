from .alerts import mcp, MBTA_API_BASE
from .alerts_request import make_alerts_request, format_useful_alerts, format_all_alerts

@mcp.tool()
async def get_mbta_alerts() -> str:
    """Get MBTA alerts (filtered to important active alerts only).
    """
    url = f"{MBTA_API_BASE}/alerts"
    data = await make_alerts_request(url)

    if not data or "data" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["data"]:
        return "No active alerts."

    result = format_useful_alerts(data["data"])
    
    if not result or result.strip() == "":
        return "No important active alerts at this time."
    
    return result