from flask import Blueprint, render_template, request, redirect, url_for, flash
from .weather_api import get_weather_data, get_forecast_data
from datetime import datetime
from .models import WeatherSearchHistory
from app import db

# Define the blueprint for main routes
main = Blueprint("main", __name__)

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

    # Store the weather data in the history with a timestamp in the database
    weather_entry = WeatherSearchHistory(
        city=city,
        temperature=weather_data.get("temperature"),
        weather=weather_data.get("weather"),
        humidity=weather_data.get("humidity"),
        icon=weather_data.get("icon"),
        latitude=weather_data.get("latitude"),
        longitude=weather_data.get("longitude"),
        date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )
    
    db.session.add(weather_entry)
    db.session.commit()

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
    Displays the session's historical weather data from the database.
    """
    search_history = WeatherSearchHistory.query.all()
    return render_template("history.html", history=search_history)


@main.route("/delete_history", methods=["POST"])
def delete_history():
    """
    Deletes a city from the weather search history.
    """
    city_to_delete = request.form.get("city")
    if city_to_delete:
        WeatherSearchHistory.query.filter_by(city=city_to_delete).delete()
        db.session.commit()
    return redirect(url_for("main.history"))
