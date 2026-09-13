"""
Web UI (Flask) for the python-weather-app.

Run with:  python web_app.py
Then open: http://127.0.0.1:5000

The API key stays server-side — it is only read in config.py and used inside
weather_service.py, never shipped to the browser.
"""
from flask import Flask, jsonify, render_template, request
from pathlib import Path

import weather_service as ws
from config import API_KEY

# Anchor the Flask instance and template lookup to this file's directory so the
# app can be launched from any working directory.
BASE_DIR = Path(__file__).resolve().parent
app = Flask(__name__, template_folder=str(BASE_DIR / "templates"))

# Fail fast with a clear message instead of a confusing 500 crash-loop when the
# user hasn't configured their key yet.
if not API_KEY:
    raise RuntimeError(
        "API_KEY not found. Create a .env file in the project root with "
        "API_KEY=your_openweather_key and restart the app."
    )


@app.route("/")
def index():
    return render_template("index.html")


def _error_response(result):
    """Map a weather_service sentinel to a clear JSON error (else None)."""
    if result == ws.AUTH_ERROR:
        return jsonify({
            "error": "auth",
            "message": "Your OpenWeather API key is being rejected. Open .env "
                       "and confirm API_KEY is your real key from "
                       "https://home.openweathermap.org/api_keys.",
        }), 401
    if result == ws.RATE_LIMITED:
        return jsonify({
            "error": "rate_limited",
            "message": "OpenWeather's free tier throttled the request. "
                       "Wait about a minute and try again.",
        }), 429
    return None


@app.route("/api/weather")
def api_weather():
    """Structured current weather for a city."""
    city = request.args.get("city", "").strip()
    if not city:
        return jsonify({"error": "missing_city", "message": "City is required."}), 400

    data = ws.get_weather_data(city)
    sentinel = _error_response(data)
    if sentinel is not None:
        return sentinel
    if data is False:
        return jsonify({"error": "network", "message": "Could not reach the weather service."}), 502
    if data is None:
        return jsonify({"error": "not_found", "message": "City not found. Try another name."}), 404

    # Share history with the CLI: record every successful web search too,
    # reusing the same display-string shape that the CLI writes to history.txt.
    record = {
        "City": data["city"],
        "Country": data["country"],
        "Temperature": f"{data['temp_c']} °C",
        "Feels Like": f"{data['feels_like_c']} °C",
        "Humidity": f"{data['humidity']} %",
        "Wind Speed": f"{data['wind_ms']} m/s",
        "Sunrise": data["sunrise"],
        "Sunset": data["sunset"],
    }
    ws.save_history(record)
    return jsonify(data)


@app.route("/api/forecast")
def api_forecast():
    """Structured 5-day forecast for a city."""
    city = request.args.get("city", "").strip()
    if not city:
        return jsonify({"error": "missing_city", "message": "City is required."}), 400

    result = ws.get_forecast_data(city)
    sentinel = _error_response(result)
    if sentinel is not None:
        return sentinel
    if result is False:
        return jsonify({"error": "network", "message": "Could not reach the weather service."}), 502
    if result is None:
        return jsonify({"error": "not_found", "message": "City not found. Try another name."}), 404

    return jsonify(result)


@app.route("/api/geocode")
def api_geocode():
    """Autocomplete city suggestions from the OpenWeather geocoding API."""
    q = request.args.get("q", "").strip()
    if not q:
        return jsonify([])
    return jsonify(ws.get_city_suggestions(q))


@app.route("/api/history")
def api_history():
    """Structured list of past searches."""
    return jsonify(ws.get_history())


@app.route("/api/history", methods=["DELETE"])
def api_clear_history():
    """Clear the search history file."""
    ws.clear_history()
    return jsonify({"ok": True})


@app.route("/api/health")
def api_health():
    """Lets the frontend check whether an API key is configured."""
    return jsonify({"api_key": bool(API_KEY)})


if __name__ == "__main__":
    app.run(debug=True)