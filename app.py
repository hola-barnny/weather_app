from flask import Flask, redirect, render_template, request, url_for
from datetime import datetime
from app.weather_api import get_weather_data
from app import create_app, db
from app.models import WeatherSearchHistory
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Validate SECRET_KEY
secret_key = os.getenv("SECRET_KEY")
if not secret_key or len(secret_key) < 32:
    raise ValueError("Invalid SECRET_KEY. Ensure it's at least 32 characters long.")

# Create the app instance
app = create_app()
app.config["SECRET_KEY"] = secret_key

# Initialize database and migration
migrate = Migrate(app, db)

def save_weather_history(weather_entry):
    """Save weather data to the database."""
    weather_record = WeatherSearchHistory(
        city=weather_entry["city"],
        temperature=weather_entry["temperature"],
        weather=weather_entry["weather"],
        humidity=weather_entry["humidity"],
        icon=weather_entry["icon"],
        date=weather_entry["date"]
    )
    db.session.add(weather_record)
    db.session.commit()

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        city = request.form.get("city")
        if not city:
            return render_template("index.html", error="City name is required.")

        weather_data = get_weather_data(city)
        if weather_data:
            weather_entry = {
                "city": city,
                "temperature": weather_data["temperature"],
                "weather": weather_data["weather"],
                "humidity": weather_data["humidity"],
                "icon": weather_data["icon"],
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            save_weather_history(weather_entry)
            return redirect(url_for("forecast", city=city))
        else:
            logger.error(f"Weather data not found for city: {city}")
            return render_template("index.html", error="City not found or invalid. Please try again.")

    return render_template("index.html")

@app.route("/forecast")
def forecast():
    city = request.args.get("city")
    if not city:
        return redirect(url_for("home"))

    weather_data = get_weather_data(city)
    if weather_data:
        # Replace with API-driven forecast data
        forecast_data = [
            {"date": "2024-12-08", "temperature": weather_data["temperature"] + 2, "weather": "Clear"},
            {"date": "2024-12-09", "temperature": weather_data["temperature"] - 1, "weather": "Partly cloudy"},
            {"date": "2024-12-10", "temperature": weather_data["temperature"], "weather": "Rainy"},
        ]
        return render_template("forecast.html", city=city, weather=weather_data, forecast=forecast_data)
    else:
        logger.error(f"Failed to retrieve forecast for city: {city}")
        return render_template("index.html", error="Unable to retrieve forecast data.")

@app.route("/map")
def map_view():
    city = request.args.get("city")
    if not city:
        return redirect(url_for("home"))

    weather_data = get_weather_data(city)
    if weather_data:
        return render_template("map.html", city=city, weather=weather_data)
    else:
        logger.error(f"Map view failed for city: {city}")
        return render_template("index.html", error="City not found or invalid. Please try again.")

@app.route("/history")
def history():
    history_data = WeatherSearchHistory.query.all()
    return render_template("history.html", history=history_data)

@app.route("/delete_history", methods=["POST"])
def delete_history():
    city_to_delete = request.form.get("city")
    WeatherSearchHistory.query.filter_by(city=city_to_delete).delete()
    db.session.commit()
    return redirect(url_for("history"))

if __name__ == "__main__":
    app.run(debug=False)
