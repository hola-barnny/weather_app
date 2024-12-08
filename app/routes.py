from flask import Blueprint, render_template, request, redirect, url_for
from .weather_api import get_weather_data, get_forecast_data
from datetime import datetime

# Define the blueprint for main routes
main = Blueprint("main", __name__)

# Mock database for weather history
weather_history = []


@main.route("/")
def home():
    """
    Renders the home page for the Weather App.
    Allows users to enter a city to fetch weather details.
    """
    return render_template("index.html")


@main.route("/", methods=["POST"])
def fetch_weather():
    """
    Handles the POST request to fetch weather data for a specified city.
    Redirects to the forecast page if successful or reloads the home page with an error message.
    """
    city = request.form.get("city")
    if not city:
        return render_template("index.html", error="City name is required.")

    weather_data = get_weather_data(city)

    if "error" in weather_data:
        return render_template("index.html", error=weather_data["error"])

    # Save weather data to the history with a timestamp
    weather_entry = {
        "city": city,
        "temperature": weather_data['temperature'],
        "weather": weather_data['weather'],
        "humidity": weather_data['humidity'],
        "icon": weather_data['icon'],
        "latitude": weather_data['latitude'],
        "longitude": weather_data['longitude'],
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    weather_history.append(weather_entry)

    # Redirect to the forecast page with the city as a parameter
    return redirect(url_for("main.forecast", city=city))


@main.route("/forecast")
def forecast():
    """
    Displays the weather forecast for a specified city.
    Fetches current weather and a 3-day forecast.
    """
    city = request.args.get("city")
    if not city:
        return redirect(url_for("main.home"))

    weather_data = get_weather_data(city)
    if "error" in weather_data:
        return render_template("index.html", error=weather_data["error"])

    forecast_data = get_forecast_data(city)
    return render_template("forecast.html", weather=weather_data, forecast=forecast_data)


@main.route("/history")
def history():
    """
    Displays the historical weather data stored during the session.
    """
    return render_template("history.html", history=weather_history)


@main.route("/map")
def map_view():
    """
    Displays an interactive map showing weather conditions for a specified city.
    Uses latitude and longitude fetched from the weather data.
    """
    city = request.args.get("city")
    if not city:
        return redirect(url_for("main.home"))

    weather_data = get_weather_data(city)
    if "error" in weather_data:
        return render_template("index.html", error=weather_data["error"])

    return render_template("map.html", city=city, weather=weather_data)
