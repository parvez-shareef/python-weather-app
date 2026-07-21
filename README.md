# python-weather-app
A Python command-line application that provides real-time weather updates and a 5-day forecast using the OpenWeather API.
# Weather CLI Application

## Overview

Weather CLI Application is a command-line application developed in Python that provides real-time weather information and a 5-day weather forecast using the OpenWeather API. The application features a menu-driven interface, maintains a searchable history of successful weather lookups, and includes robust error handling for network and invalid input scenarios.

This project was built to strengthen practical knowledge of working with REST APIs, JSON data, modular programming, file handling, and exception handling in Python.

---

## Features

* View current weather for any supported city
* Display a 5-day weather forecast
* Save successful weather searches to a history file
* View previously saved search history
* Clear search history
* Display:

  * Temperature
  * Feels Like temperature
  * Humidity
  * Wind Speed
  * Sunrise time
  * Sunset time
* Handle invalid city names gracefully
* Handle network connection failures
* Interactive menu-driven command-line interface

---

## Technologies Used

* Python 3
* Requests
* OpenWeather API
* File Handling
* Exception Handling
* Python Modules and Functions

---

## Project Structure

```text
weather-app/
│
├── main.py
├── weather_service.py
├── config.py
├── history.txt
├── requirements.txt
├── README.md
├── .gitignore
└── .env
```

---

## Installation

Clone the repository:

```bash
# Weather CLI Application

## Overview

Weather CLI Application is a command-line application developed in Python that provides real-time weather information and a 5-day weather forecast using the OpenWeather API. The application features a menu-driven interface, maintains a searchable history of successful weather lookups, and includes robust error handling for network and invalid input scenarios.

This project was built to strengthen practical knowledge of working with REST APIs, JSON data, modular programming, file handling, and exception handling in Python.

---

## Features

* View current weather for any supported city
* Display a 5-day weather forecast
* Save successful weather searches to a history file
* View previously saved search history
* Clear search history
* Display:

  * Temperature
  * Feels Like temperature
  * Humidity
  * Wind Speed
  * Sunrise time
  * Sunset time
* Handle invalid city names gracefully
* Handle network connection failures
* Interactive menu-driven command-line interface

---

## Technologies Used

* Python 3
* Requests
* OpenWeather API
* File Handling
* Exception Handling
* Python Modules and Functions

---

## Project Structure

```text
weather-app/
│
├── main.py
├── weather_service.py
├── config.py
├── history.txt
├── requirements.txt
├── README.md
├── .gitignore
└── .env
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/weather-app.git
```

Navigate to the project directory:

```bash
cd weather-app
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

## API Configuration

Create a `.env` file in the project directory and add your OpenWeather API key.

```env
API_KEY=YOUR_API_KEY
```

---

## Running the Application

Execute the following command:

```bash
python main.py
```

---

## Sample Output

```text
=========================
   WEATHER APPLICATION
=========================

1. Search Weather
2. View Search History
3. Clear Search History
4. Exit

Choose an option: 1

Enter your city name: Hyderabad

Searching weather for Hyderabad...

-------------------------
     WEATHER REPORT
-------------------------

City            : Hyderabad
Country         : IN
Temperature     : 29 °C
Feels Like      : 31 °C
Humidity        : 67 %
Wind Speed      : 2.5 m/s
Sunrise         : 05:48 AM
Sunset          : 06:52 PM

-------------------------
     NEXT 5 FORECASTS
-------------------------

Date            : 2026-07-22
Temperature     : 30 °C
Description     : Broken Clouds
```

---

## Learning Outcomes

This project provided practical experience with:

* Consuming REST APIs
* Parsing and processing JSON responses
* Writing modular and reusable Python code
* Working with functions and modules
* Using dictionaries and lists effectively
* File operations (read, write, and append)
* Exception handling
* Building interactive command-line applications
* Organizing a Python project for GitHub

---

## Future Improvements

Potential enhancements include:

* Hourly weather forecast
* Automatic location detection
* Support for multiple temperature units
* Weather icons in the terminal
* Export weather reports to PDF or CSV
* Graphical user interface (GUI)
* Data visualization for weather trends

---

## Requirements

* Python 3.10 or later
* Internet connection
* OpenWeather API Key

---

## License

This project is intended for educational and learning purposes.

---

## Author

**Mohammed Parvez Sharif**

Computer Science Engineering Student

GitHub: https://github.com/your-username

```

Navigate to the project directory:

```bash
cd weather-app
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

## API Configuration

Create a `.env` file in the project directory and add your OpenWeather API key.

```env
API_KEY=YOUR_API_KEY
```

---

## Running the Application

Execute the following command:

```bash
python main.py
```

---

## Sample Output

```text
=========================
   WEATHER APPLICATION
=========================

1. Search Weather
2. View Search History
3. Clear Search History
4. Exit

Choose an option: 1

Enter your city name: Hyderabad

Searching weather for Hyderabad...

-------------------------
     WEATHER REPORT
-------------------------

City            : Hyderabad
Country         : IN
Temperature     : 29 °C
Feels Like      : 31 °C
Humidity        : 67 %
Wind Speed      : 2.5 m/s
Sunrise         : 05:48 AM
Sunset          : 06:52 PM

-------------------------
     NEXT 5 FORECASTS
-------------------------

Date            : 2026-07-22
Temperature     : 30 °C
Description     : Broken Clouds
```

---

## Learning Outcomes

This project provided practical experience with:

* Consuming REST APIs
* Parsing and processing JSON responses
* Writing modular and reusable Python code
* Working with functions and modules
* Using dictionaries and lists effectively
* File operations (read, write, and append)
* Exception handling
* Building interactive command-line applications
* Organizing a Python project for GitHub

---

## Future Improvements

Potential enhancements include:

* Hourly weather forecast
* Automatic location detection
* Support for multiple temperature units
* Weather icons in the terminal
* Export weather reports to PDF or CSV
* Graphical user interface (GUI)
* Data visualization for weather trends

---

## Requirements

* Python 3.10 or later
* Internet connection
* OpenWeather API Key

---

## License

This project is intended for educational and learning purposes.

---

## Author

**Mohammed Parvez Shareef**

Computer Science Engineering Student

github: https://github.com/parvez-shareef
