# run.py
from flask import Flask, render_template, request, redirect, url_for
from app.utils import get_weather_data, save_weather_history, get_search_history  # Import functions from utils.py
from app.weather_api import get_weather_from_api  # Import weather API helper
from app.models import WeatherSearchHistory  # Import model if using a database
from datetime import datetime
import requests

# Initialize Flask app
app = Flask(__name__)

# Initialize the weather history storage (could be replaced with database)
weather_history = []

# Function to fetch weather data from OpenWeatherMap API
def get_weather_data(city):
    API_KEY = "your_openweathermap_api_key"  # Replace with your OpenWeatherMap API key
    WEATHER_API_URL = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(WEATHER_API_URL)
    data = response.json()

    # Return weather data in a structured format
    if response.status_code == 200:
        return {
            "temperature": data['main']['temp'],
            "weather": data['weather'][0]['description'],
            "humidity": data['main']['humidity'],
            "icon": data['weather'][0]['icon'],
            "latitude": data['coord']['lat'],
            "longitude": data['coord']['lon']
        }
    else:
        return None

# Route for the home page (index.html)
@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        city = request.form.get("city")
        weather_data = get_weather_data(city)

        if weather_data:
            weather_entry = {
                "city": city,
                "temperature": weather_data['temperature'],
                "weather": weather_data['weather'],
                "humidity": weather_data['humidity'],
                "icon": weather_data['icon'],
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            weather_history.append(weather_entry)
            return redirect(url_for("forecast", city=city))  # Redirect to forecast page
        else:
            error_message = "City not found or invalid. Please try again."
            return render_template("index.html", error=error_message)

    return render_template("index.html")

# Route for weather forecast page (forecast.html)
@app.route("/forecast")
def forecast():
    city = request.args.get("city")
    weather_data = get_weather_data(city)

    if weather_data:
        forecast_data = [
            {"date": "2024-12-08", "temperature": weather_data['temperature'] + 2, "weather": "Clear"},
            {"date": "2024-12-09", "temperature": weather_data['temperature'] - 1, "weather": "Partly cloudy"},
            {"date": "2024-12-10", "temperature": weather_data['temperature'], "weather": "Rainy"}
        ]
        return render_template("forecast.html", city=city, weather=weather_data, forecast=forecast_data)
    else:
        error_message = "Unable to retrieve forecast data."
        return render_template("index.html", error=error_message)

# Route for the weather map page (map.html)
@app.route("/map")
def map_view():
    city = request.args.get("city")
    weather_data = get_weather_data(city)

    if weather_data:
        return render_template("map.html", city=city, weather=weather_data)
    else:
        error_message = "City not found or invalid. Please try again."
        return render_template("index.html", error=error_message)

# Route for weather history page (history.html)
@app.route("/history")
def history():
    return render_template("history.html", history=weather_history)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
