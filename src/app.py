# src/app.py
from flask import Flask, render_template, jsonify, request
from database import get_city_rows, save_record_to_db
from fetcher import get_coordinates_for_city, fetch_weather

app = Flask(__name__)


@app.route("/")
def index():
    # short list for the demo
    cities = ["Addis Ababa", "Nairobi", "Cairo", "Lagos",
              "Yangon", "Berlin", "New York", "Tokyo",]
    return render_template("dashboard.html", cities=cities)


@app.route("/api/weather/<city>")
def api_weather(city):
    # return recent rows as simple JSON
    rows = get_city_rows(city, limit=50)
    return jsonify([{"time": r[0], "temp": r[1]} for r in rows])


@app.route("/api/live-weather", methods=["POST"])
def api_live_weather():
    # expects JSON: {"city": "Berlin"}
    payload = request.get_json(silent=True) or {}
    city = payload.get("city")
    if not city:
        return jsonify({"error": "need city"}), 400

    coords = get_coordinates_for_city(city)
    if not coords:
        return jsonify({"error": "city not found"}), 404

    record = fetch_weather(city, coords["latitude"], coords["longitude"])
    if not record:
        return jsonify({"error": "fetch failed"}), 500

    save_record_to_db(record)   # keep it simple
    return jsonify({
        "city": record["city"],
        "temp": record["temperature_c"],
        "wind": record["windspeed_ms"],
        "time": record["timestamp"]
    })


if __name__ == "__main__":
    print("Run: http://127.0.0.1:5000")
    app.run(debug=True)
