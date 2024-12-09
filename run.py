from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from app.weather_api import get_weather 
from app.utils import save_weather_history, get_search_history 
from app.models import WeatherSearchHistory
from flask_sqlalchemy import SQLAlchemy
import os
from app import app, db
from flask_migrate import Migrate

# Initialize the Flask app
app = Flask(__name__)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:JasonZoe@1985@localhost/weatherapp_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy and Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Route for the home page (index.html)
@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        city = request.form.get("city")
        weather_data = get_weather(city)

        if weather_data:
            weather_entry = {
                "city": city,
                "temperature": weather_data['temperature'],
                "weather": weather_data['weather'],
                "humidity": weather_data['humidity'],
                "icon": weather_data['icon'],
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            # Save weather entry to the database
            save_weather_history(weather_entry)
            return redirect(url_for("forecast", city=city))
        else:
            error_message = "City not found or invalid. Please try again."
            return render_template("index.html", error=error_message)

    return render_template("index.html")

# Route for the weather forecast page (forecast.html)
@app.route("/forecast")
def forecast():
    city = request.args.get("city")
    weather_data = get_weather(city)

    if weather_data:
        # Mock forecast data (you would get actual forecast from an API in a real application)
        forecast_data = [
            {"date": "2024-12-08", "temperature": weather_data['temperature'] + 2, "weather": "Clear"},
            {"date": "2024-12-09", "temperature": weather_data['temperature'] - 1, "weather": "Partly cloudy"},
            {"date": "2024-12-10", "temperature": weather_data['temperature'], "weather": "Rainy"}
        ]
        return render_template("forecast.html", city=city, weather=weather_data, forecast=forecast_data)
    else:
        error_message = "Unable to retrieve forecast data."
        return render_template("index.html", error=error_message)

# Route for the weather history page (history.html)
@app.route("/history")
def history():
    history = get_search_history()
    return render_template("history.html", history=history)

# Function to save weather search history to the database
def save_weather_history(weather_data):
    new_entry = WeatherSearchHistory(
        city=weather_data['city'],
        temperature=weather_data['temperature'],
        weather=weather_data['weather'],
        humidity=weather_data['humidity'],
        icon=weather_data['icon'],
        date=weather_data['date']
    )
    db.session.add(new_entry)
    db.session.commit()

# Function to get all search history from the database
def get_search_history():
    history = WeatherSearchHistory.query.all()
    return history

# Run the Flask app
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
