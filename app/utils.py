import requests
from datetime import datetime
import os

# Function to fetch weather data from OpenWeatherMap API
def get_weather_data(city):
    try:
        # OpenWeatherMap API endpoint and your API key
        API_KEY = 'd9fea7939f24f617ce85b4327a724acc'
        WEATHER_API_URL = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        
        # Make a GET request to fetch the data
        response = requests.get(WEATHER_API_URL)
        data = response.json()
        
        # Handle API errors like invalid city name
        if data['cod'] != 200:
            raise ValueError("City not found.")
        
        # Extracting relevant weather information
        weather_info = {
            'city': city,
            'temperature': data['main']['temp'],
            'weather': data['weather'][0]['description'],
            'humidity': data['main']['humidity'],
            'icon': data['weather'][0]['icon'],
            'latitude': data['coord']['lat'],
            'longitude': data['coord']['lon'],
        }
        
        return weather_info
    
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return None

# Function to save search history into the database
def save_weather_history(weather_data):
    try:
        # Delay imports to avoid circular dependency issues
        from app import db
        from app.models import WeatherSearchHistory

        history_entry = WeatherSearchHistory(
            city=weather_data['city'],
            temperature=weather_data['temperature'],
            weather=weather_data['weather'],
            humidity=weather_data['humidity'],
            icon=weather_data['icon'],
            latitude=weather_data['latitude'],
            longitude=weather_data['longitude'],
            date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        
        # Save the entry to the database
        db.session.add(history_entry)
        db.session.commit()
        print(f"Weather history for {weather_data['city']} saved successfully.")
        
    except Exception as e:
        print(f"Error saving weather history: {e}")

# Function to retrieve search history from the database
def get_search_history():
    try:
        # Delay imports to avoid circular dependency issues
        from app.models import WeatherSearchHistory

        # Fetch all weather search history from the database
        history = WeatherSearchHistory.query.all()
        return [entry.to_dict() for entry in history]
    except Exception as e:
        print(f"Error fetching history: {e}")
        return []
