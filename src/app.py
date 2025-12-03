from fetcher import get_coordinates_for_city, fetch_weather, fetch_forecast
from database import get_city_rows, save_record_to_db
from flask import Flask, render_template, jsonify, request
import sqlite3


app = Flask(__name__)


@app.route('/')
def dashboard():
    cities = ["Ankara", "Beijing", "Berlin", "Brasília", "London", "Madrid", "Mexico City", "Moscow",
              "New Delhi", "Ottawa", "Paris", "Pretoria", "Riyadh", "Rome", "Seoul", "Tokyo", "Washington, D.C."]

    return render_template('dashboard.html', cities=cities)


@app.route('/api/weather/<city>')
def weather_data(city):
    """Get historical data for charts"""
    rows = get_city_rows(city, limit=50)
    data = [{"time": row[0], "temperature": row[1]} for row in rows]
    return jsonify(data)


@app.route('/api/forecast/<city>')
def forecast_data(city):
    """Get 5-day forecast for a city"""
    coords = get_coordinates_for_city(city)
    if not coords:
        return jsonify({"error": "City not found"}), 404

    forecast = fetch_forecast(coords["latitude"], coords["longitude"])
    if forecast:
        return jsonify(forecast.get("daily", {}))
    return jsonify({"error": "No forecast data"}), 500


@app.route('/api/live-weather', methods=['POST'])
def live_weather():
    """Get LIVE weather data for any city"""
    city_name = request.json.get('city')

    if not city_name:
        return jsonify({"error": "No city provided"}), 400

    # Get coordinates for the city
    coords = get_coordinates_for_city(city_name)
    if not coords:
        return jsonify({"error": f"City '{city_name}' not found"}), 404

    # Fetch LIVE weather data
    live_data = fetch_weather(
        city_name, coords["latitude"], coords["longitude"])

    if live_data:
        # Save to database for historical tracking
        save_record_to_db(live_data)
        return jsonify({
            "city": live_data["city"],
            "temperature": live_data["temperature_c"],
            "windspeed": live_data["windspeed_ms"],
            "humidity": live_data["humidity_percent"],
            "cloudcover": live_data["cloudcover_percent"],
            "timestamp": live_data["timestamp"]
        })
    else:
        return jsonify({"error": "Failed to fetch weather data"}), 500


if __name__ == '__main__':
    print("Starting Weather Dashboard...")
    print("Visit: http://localhost:5000")
    app.run(debug=True)
