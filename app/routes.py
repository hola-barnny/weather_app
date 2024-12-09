from flask import Blueprint, render_template, request, redirect, url_for, flash
from .weather_api import get_weather_data, get_forecast_data
from datetime import datetime

# Define the blueprint for main routes
main = Blueprint("main", __name__)

# In-memory storage for weather history (for demonstration purposes)
weather_history = []

@main.route("/")
def index():
    """
    Renders the home page for the Weather App.
    Allows users to input a city to fetch weather details.
    """
    return render_template("index.html")


@main.route("/", methods=["POST"])
def fetch_weather():
    """
    Handles the form submission to fetch weather data for a given city.
    Saves the data to weather history and redirects to the forecast page.
    """
    city = request.form.get("city")
    if not city:
        flash("City name is required.", "error")
        return redirect(url_for("main.index"))

    # Fetch weather data from the API
    weather_data = get_weather_data(city)

    if "error" in weather_data:
        flash(weather_data["error"], "error")
        return redirect(url_for("main.index"))

    # Store the weather data in the history with a timestamp
    weather_entry = {
        "city": city,
        "temperature": weather_data.get("temperature"),
        "weather": weather_data.get("weather"),
        "humidity": weather_data.get("humidity"),
        "icon": weather_data.get("icon"),
        "latitude": weather_data.get("latitude"),
        "longitude": weather_data.get("longitude"),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    weather_history.append(weather_entry)

    # Redirect to the forecast page with the city as a query parameter
    return redirect(url_for("main.forecast", city=city))


@main.route("/forecast")
def forecast():
    """
    Displays the current weather and a 3-day forecast for the specified city.
    """
    city = request.args.get("city")
    if not city:
        return redirect(url_for("main.index"))

    # Fetch current weather and forecast data
    weather_data = get_weather_data(city)
    if "error" in weather_data:
        flash(weather_data["error"], "error")
        return redirect(url_for("main.index"))

    forecast_data = get_forecast_data(city)
    return render_template("forecast.html", weather=weather_data, forecast=forecast_data)


@main.route("/history")
def history():
    """
    Displays the session's historical weather data.
    """
    return render_template("history.html", history=weather_history)


@main.route("/map")
def map_view():
    """
    Displays an interactive map for the specified city's weather conditions.
    """
    city = request.args.get("city")
    if not city:
        return redirect(url_for("main.index"))

    # Fetch weather data for map view
    weather_data = get_weather_data(city)
    if "error" in weather_data:
        flash(weather_data["error"], "error")
        return redirect(url_for("main.index"))

    return render_template("map.html", city=city, weather=weather_data)
