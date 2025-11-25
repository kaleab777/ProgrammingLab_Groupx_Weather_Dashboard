import requests
from datetime import datetime, timezone

API_BASE = "https://api.open-meteo.com/v1/forecast"
Geocoding_API_BASE = "https://geocoding-api.open-meteo.com/v1/search"
TIMEOUT = 10


def get_coordinates_for_city(city_name):
    params = {
        "name": city_name,
        "count": "1",
        "language": "en",
        "format": "json"

    }

    try:
        resp = requests.get(Geocoding_API_BASE, params=params, timeout=TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        if data and "results" in data and len(data["results"]) > 0:
            first_result = data["results"][0]

            latitude = first_result.get("latitude")
            longitude = first_result.get("longitude")

            city_name = first_result.get("name")

            return {
                "city_name": city_name,
                "latitude": latitude,
                "longitude": longitude
            }

    except Exception:
        return None, None


def fetch_weather(city: str, latitude: float, longitude: float, timeout: int = 10):
    """
    Fetch current weather for the given coordinates from Open-Meteo API.
    Returns a dict with keys: city, timestamp, temperature_c, windspeed_ms, humidity_percent, cloudcover_percent, raw
    Returns None if something goes wrong.
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,windspeed_10m,relative_humidity_2m,cloud_cover,weather_code",
        "timezone": "auto"
    }

    try:
        resp = requests.get(API_BASE, params=params, timeout=timeout)
        resp.raise_for_status()
        payload = resp.json()
    except Exception:
        return None

    current = payload.get("current")
    if not current:
        return None

    # Use the fetch time in UTC as timestamp (simple and safe)
    ts = datetime.now(timezone.utc).isoformat()

    temperature = current.get("temperature_2m")
    windspeed = current.get("windspeed_10m")
    humidity = current.get("relative_humidity_2m")
    cloudcover = current.get("cloud_cover")

    return {
        "city": city,
        "timestamp": ts,
        "temperature_c": temperature,
        "windspeed_ms": windspeed,
        "humidity_percent": humidity,
        "cloudcover_percent": cloudcover,
        "raw": payload
    }


if __name__ == "__main__":
    city_name = "Berlin"
    coords = get_coordinates_for_city(city_name)
    if coords:
        print(f"Coordinates for {city_name}: {coords}")
        weather = fetch_weather(
            city_name, coords["latitude"], coords["longitude"])
        print("Fetched weather:", weather)
    else:
        print(f"Could not find coordinates for city: {city_name}")
