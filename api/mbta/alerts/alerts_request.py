from datetime import datetime
from zoneinfo import ZoneInfo
import httpx
from ..const import MBTA_API_KEY
from .alerts import USER_AGENT
from .alerts_enum import USEFUL_ALERT_ATTRIBUTES

async def make_alerts_request(url: str) -> dict:
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
        "Authorization": f"Bearer {MBTA_API_KEY}",
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            data = response.json()
            return data
        except Exception as e:
            return None

def determine_active_alerts(start: str | None, end: str | None) -> bool:
    tz = ZoneInfo("America/New_York")
    now = datetime.now(tz)

    def parse_iso(s: str | None):
        return datetime.fromisoformat(s) if s else None

    start_dt = parse_iso(start)
    end_dt = parse_iso(end)

    # Both start and end exist: check if we're in the time window
    if start_dt is not None and end_dt is not None:
        start_dt = start_dt.astimezone(tz)
        end_dt = end_dt.astimezone(tz)
        return start_dt <= now <= end_dt
    
    # Only start exists (no end): consider active if start has passed (ongoing alert)
    if start_dt is not None and end_dt is None:
        start_dt = start_dt.astimezone(tz)
        return now >= start_dt
    
    # No time info: consider inactive
    return False

def format_time_range(start: str | None, end: str | None) -> str:
    tz = ZoneInfo("America/New_York")
    now = datetime.now(tz)
    if start is not None and end is not None:
        start_dt = datetime.fromisoformat(start).astimezone(tz)
        end_dt = datetime.fromisoformat(end).astimezone(tz)
        return f"{start_dt.strftime('%I:%M %p')} - {end_dt.strftime('%I:%M %p')}"
    return None

def format_useful_alerts(alerts: dict) -> str:
    alerts_string = ""
    
    # Convert Enum values to strings for comparison
    useful_effects = [alert.value for alert in USEFUL_ALERT_ATTRIBUTES]
    
    for alert_data in alerts:
        attributes = alert_data.get("attributes", {})
        
        effect = attributes.get("effect", "UNKNOWN")
        has_active_period = "active_period" in attributes and len(attributes["active_period"]) > 0
        
        if has_active_period:
            is_active = determine_active_alerts(
                attributes["active_period"][0]["start"], 
                attributes["active_period"][0]["end"]
            )
        else:
            is_active = False
                    
        if "effect" in attributes and attributes["effect"] in useful_effects:
            if has_active_period and is_active:
                time_range = format_time_range(
                    attributes['active_period'][0]['start'], 
                    attributes['active_period'][0]['end']
                )
                alerts_string += f"{attributes['header']} - {attributes['cause']} - {attributes['effect']} - {time_range}\n"
    
    return alerts_string

def format_all_alerts(alerts: dict) -> str:
    """Format all alerts without filtering."""
    alerts_string = f"Total alerts: {len(alerts)}\n\n"
    
    for alert_data in alerts:
        attributes = alert_data.get("attributes", {})
        header = attributes.get("header", "No header")
        effect = attributes.get("effect", "UNKNOWN_EFFECT")
        cause = attributes.get("cause", "UNKNOWN_CAUSE")
        
        # Check if active
        has_active_period = "active_period" in attributes and len(attributes["active_period"]) > 0
        if has_active_period:
            is_active = determine_active_alerts(
                attributes["active_period"][0]["start"], 
                attributes["active_period"][0]["end"]
            )
            time_range = format_time_range(
                attributes['active_period'][0]['start'], 
                attributes['active_period'][0]['end']
            )
            status = "🟢 ACTIVE" if is_active else "⚪ INACTIVE"
            alerts_string += f"{status} | {effect}\n"
            alerts_string += f"  {header}\n"
            alerts_string += f"  Cause: {cause} | Time: {time_range}\n\n"
        else:
            alerts_string += f"⚪ NO TIME | {effect}\n"
            alerts_string += f"  {header}\n"
            alerts_string += f"  Cause: {cause}\n\n"
    
    return alerts_string