import requests
import datetime
from config import API_KEY


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
    with open("history.txt", "a") as fh:
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