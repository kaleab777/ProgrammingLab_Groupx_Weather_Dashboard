import requests
from datetime import datetime, timezone

API_BASE = "https://api.open-meteo.com/v1/forecast"


def fetch_weather(city: str, latitude: float, longitude: float, timeout: int = 10):

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": "true"
    }
    """
      Fetch current weather for the given coordinates from Open-Meteo.
      Returns a dict with keys: city, timestamp, temperature_c, windspeed_ms, raw
      Returns None if something goes wrong.
      """

    try:
        resp = requests.get(API_BASE, params=params, timeout=timeout)
        resp.raise_for_status()
        payload = resp.json()
    except Exception:
        return None

    current = payload.get("current_weather")
    if not current:
        return None

    # Use the fetch time in UTC as timestamp (simple and safe)
    ts = datetime.now(timezone.utc).isoformat()

    temperature = current.get("temperature")
    windspeed = current.get("windspeed")

    return {
        "city": city,
        "timestamp": ts,
        "temperature_c": temperature,
        "windspeed_ms": windspeed,
        "raw": payload
    }


if __name__ == "__main__":
    print(fetch_weather("Stuttgart", 48.78, 9.18))
