from flask import Flask, redirect, render_template, request, url_for
from datetime import datetime
from app.weather_api import get_weather_data
from app import create_app, db
from app.models import WeatherSearchHistory
from flask_migrate import Migrate
import os

# Create the app instance using the factory function
app = create_app()

# Configure SQLAlchemy
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "JasonZoe@1985")
DB_PASSWORD_ENCODED = DB_PASSWORD.replace('@', '%40')

DB_NAME = os.getenv("DB_NAME", "weatherapp_db")

# Update the DATABASE_URI to include the encoded password
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD_ENCODED}@{DB_HOST}/{DB_NAME}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database and migration
migrate = Migrate(app, db)

# Custom function to save weather data to the database
def save_weather_history(weather_entry):
    # Create a new record in the WeatherSearchHistory table
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

# Route for the home page
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
            return render_template("index.html", error="City not found or invalid. Please try again.")

    return render_template("index.html")

# Route for the weather forecast page
@app.route("/forecast")
def forecast():
    city = request.args.get("city")
    if not city:
        return redirect(url_for("home"))

    weather_data = get_weather_data(city)
    if weather_data:
        forecast_data = [
            {"date": "2024-12-08", "temperature": weather_data["temperature"] + 2, "weather": "Clear"},
            {"date": "2024-12-09", "temperature": weather_data["temperature"] - 1, "weather": "Partly cloudy"},
            {"date": "2024-12-10", "temperature": weather_data["temperature"], "weather": "Rainy"},
        ]
        return render_template("forecast.html", city=city, weather=weather_data, forecast=forecast_data)
    else:
        return render_template("index.html", error="Unable to retrieve forecast data.")

# Route for the weather map page
@app.route("/map")
def map_view():
    city = request.args.get("city")
    if not city:
        return redirect(url_for("home"))

    weather_data = get_weather_data(city)
    if weather_data:
        return render_template("map.html", city=city, weather=weather_data)
    else:
        return render_template("index.html", error="City not found or invalid. Please try again.")

# Route for the search history page
@app.route("/history")
def history():
    history_data = WeatherSearchHistory.query.all()
    return render_template("history.html", history=history_data)

# Route to delete a city from search history
@app.route("/delete_history", methods=["POST"])
def delete_history():
    city_to_delete = request.form.get("city")
    WeatherSearchHistory.query.filter_by(city=city_to_delete).delete()
    db.session.commit()  # Commit changes to DB
    return redirect(url_for("history"))

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
