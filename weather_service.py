import requests
import datetime
from pathlib import Path
from config import API_KEY

# Anchor file paths to the project root so history is shared no matter where
# the app (CLI or web) is launched from.
BASE_DIR = Path(__file__).resolve().parent
HISTORY_FILE = BASE_DIR / "history.txt"

# Sentinel return values used by the web-facing helpers to distinguish API-key
# problems from a genuinely unknown city (which would otherwise be reported as
# "city not found" for every request).
AUTH_ERROR = "auth_error"        # OpenWeather rejects the API key (HTTP 401/403)
RATE_LIMITED = "rate_limited"    # free-tier call limit reached (HTTP 429)


def get_forecast(city):
    """
    Fetches the 5-day weather forecast for the specified city.

    Parameters:
        city (str): Name of the city.

    Returns:
        list: A list of dictionaries containing the forecast for each day.
        None: If the city name is invalid or not found.
        False: If a network error occurs.
    """
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        if str(data["cod"]) != "200":
            return None

        forecast = []
        shown_dates = set()

        for forecast_item in data["list"]:

            date = forecast_item["dt_txt"].split()[0]

            if date in shown_dates:
                continue

            shown_dates.add(date)

            weather_forecast = {
                "📅 Date": date,
                "🌡️ Temperature": f"{forecast_item['main']['temp']} °C",
                "☁️ Description": forecast_item["weather"][0]["description"].title()
            }

            forecast.append(weather_forecast)

        return forecast

    except requests.exceptions.RequestException:
        return False

def get_weather(city):
    # docstring
    """
    Fetches the current weather for the specified city.

    Parameters:
        city (str): Name of the city.

    Returns:
        dict: Current weather information if the request is successful.
        None: If the city name is invalid or not found.
        False: If a network error occurs.
    """
    #code
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        # Compare as string
        if str(data["cod"]) != "200":
            return None

        now = datetime.datetime.now()
        searched_time = now.strftime("%I:%M %p %d/%m/%Y")

        sunrise = datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"]
        ).strftime("%I:%M %p")

        sunset = datetime.datetime.fromtimestamp(
            data["sys"]["sunset"]
        ).strftime("%I:%M %p")

        weather = {
            "City": city.title(),
            "Country": data["sys"]["country"],
            "Temperature": f"{data['main']['temp']} °C",
            "Feels Like": f"{data['main']['feels_like']} °C",
            "Humidity": f"{data['main']['humidity']} %",
            "Wind Speed": f"{data['wind']['speed']} m/s",
            "Sunrise": sunrise,
            "Sunset": sunset,
        }

        print(f"Searched at {searched_time}")

        return weather

    except requests.exceptions.RequestException:
        return False
def save_history(weather):
    with open(HISTORY_FILE, "a", encoding="utf-8") as fh:
        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime("%d-%m-%Y %I:%M %p")

        fh.write(f"searched at {formatted_time}\n")

        for key, value in weather.items():
            fh.write(f"{key:<15}: {value}\n")

        fh.write("-" * 40 + "\n\n")
def view_history():
    """"displays the saved weather history """
    try:
         with open("history.txt",'r') as file:
           history=file.read()
           print("\n YOUR SEARCHED HISTORY IS:\n")
           if history:
            print(history)
           else:
            print("no searched history found")
    except FileNotFoundError:
        print("you did not have any searchd history")      
# ---------------------------------------------------------------------------
# Structured helpers for the web UI (Flask)
# These return clean numeric/structured data instead of display strings and
# never print to stdout. The CLI functions above are left untouched.
# ---------------------------------------------------------------------------

def get_weather_data(city):
    """
    Fetches current weather for the web UI as structured data.

    Returns:
        dict: { city, country, condition, icon, temp_c, feels_like_c, humidity,
                wind_ms, sunrise, sunset, searched_at }
        None: If the city name is invalid or not found.
        False: If a network error occurs.
    """
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        cod = str(data.get("cod"))
        if cod == "401" or cod == "403":
            return AUTH_ERROR
        if cod == "429":
            return RATE_LIMITED
        if cod != "200":
            return None

        now = datetime.datetime.now()

        return {
            "city": data["name"],
            "country": data["sys"]["country"],
            "condition": data["weather"][0]["description"].title(),
            "icon": data["weather"][0]["icon"],
            "temp_c": data["main"]["temp"],
            "feels_like_c": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "wind_ms": data["wind"]["speed"],
            "sunrise": datetime.datetime.fromtimestamp(
                data["sys"]["sunrise"]).strftime("%I:%M %p"),
            "sunset": datetime.datetime.fromtimestamp(
                data["sys"]["sunset"]).strftime("%I:%M %p"),
            "searched_at": now.strftime("%I:%M %p %d/%m/%Y"),
        }

    except requests.exceptions.RequestException:
        return False


def get_forecast_data(city):
    """
    Fetches the 5-day forecast as structured per-day data for the web UI.

    The forecast endpoint returns 3-hourly blocks, so blocks are grouped by
    date and the daily min/max temps are computed across them.

    Returns:
        dict: { city, country, days: [ per-day weather ] }
        None: If the city name is invalid or not found.
        False: If a network error occurs.
    """
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        cod = str(data.get("cod"))
        if cod == "401" or cod == "403":
            return AUTH_ERROR
        if cod == "429":
            return RATE_LIMITED
        if cod != "200":
            return None

        days = {}
        for item in data["list"]:
            day = item["dt_txt"].split()[0]

            if day not in days:
                days[day] = {
                    "date": day,
                    "icon": item["weather"][0]["icon"],
                    "condition": item["weather"][0]["description"].title(),
                    "temp_min_c": item["main"]["temp_min"],
                    "temp_max_c": item["main"]["temp_max"],
                    "humidity": item["main"]["humidity"],
                    "wind_ms": item["wind"]["speed"],
                }
                continue

            entry = days[day]
            entry["temp_min_c"] = min(entry["temp_min_c"], item["main"]["temp_min"])

            # Represent the dominant daytime condition with the warmest block.
            if item["main"]["temp_max"] > entry["temp_max_c"]:
                entry["temp_max_c"] = item["main"]["temp_max"]
                entry["icon"] = item["weather"][0]["icon"]
                entry["condition"] = item["weather"][0]["description"].title()

            entry["humidity"] = max(entry["humidity"], item["main"]["humidity"])
            entry["wind_ms"] = max(entry["wind_ms"], item["wind"]["speed"])

        return {
            "city": data["city"]["name"],
            "country": data["city"].get("country", ""),
            "days": [days[day] for day in sorted(days)],
        }

    except requests.exceptions.RequestException:
        return False


def get_city_suggestions(q):
    """
    Returns autocomplete city suggestions from the OpenWeather geocoding API.

    Returns:
        list: [{ name, country, state (optional) }, ...]; empty if none/error.
    """
    if not API_KEY:
        return []

    url = f"http://api.openweathermap.org/geo/1.0/direct?q={q}&limit=5&appid={API_KEY}"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()
    except (requests.exceptions.RequestException, ValueError):
        return []

    suggestions = []
    for item in data:
        suggestion = {
            "name": item.get("name", ""),
            "country": item.get("country", ""),
        }
        if item.get("state"):
            suggestion["state"] = item["state"]
        suggestions.append(suggestion)
    return suggestions


def get_history():
    """
    Parses history.txt into a structured list of entries.

    Returns:
        list: [{ searched_at: str, City: str, Country: str, ... }, ...]
        An empty list when there is no history file yet.
    """
    entries = []
    if not HISTORY_FILE.exists():
        return entries

    current = None
    with open(HISTORY_FILE, "r", encoding="utf-8") as fh:
        for raw in fh:
            line = raw.rstrip("\n")

            if line.startswith("searched at "):
                current = {"searched_at": line[len("searched at "):]}
                entries.append(current)
            elif ": " in line and current is not None:
                key, _, value = line.partition(": ")
                current[key.strip()] = value.strip()
            else:
                # Dashed separator or blank line ends the current entry.
                current = None

    # Newest searches first — the natural order for a UI list.
    return list(reversed(entries))


def clear_history():
    """Empties (or creates) history.txt. Returns True when the file is empty."""
    with open(HISTORY_FILE, "w", encoding="utf-8") as fh:
        pass
    return True
