import requests
from app.models import db, WeatherSearchHistory  # Import db and model from the app package
from datetime import datetime

# Function to fetch weather data from OpenWeatherMap API
def get_weather_data(city):
    try:
        # OpenWeatherMap API endpoint and your API key
        API_KEY = 'your_openweathermap_api_key'  # Replace with your actual API key
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
            'temperature': data['main']['temp'],  # Temperature in Celsius
            'weather': data['weather'][0]['description'],  # Weather condition
            'humidity': data['main']['humidity'],  # Humidity percentage
            'icon': data['weather'][0]['icon'],  # Weather icon
            'latitude': data['coord']['lat'],  # Latitude
            'longitude': data['coord']['lon'],  # Longitude
        }
        
        return weather_info
    
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return None

# Function to save search history into the database
def save_weather_history(weather_data):
    try:
        # Create a new history entry and add it to the session
        history_entry = WeatherSearchHistory(
            city=weather_data['city'],
            temperature=weather_data['temperature'],
            weather=weather_data['weather'],
            humidity=weather_data['humidity'],
            icon=weather_data['icon'],
            latitude=weather_data['latitude'],
            longitude=weather_data['longitude'],
            date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Current timestamp
        )
        
        # Add and commit the new history entry to the database
        db.session.add(history_entry)
        db.session.commit()
        print(f"Weather history for {weather_data['city']} saved successfully.")
        
    except Exception as e:
        print(f"Error saving weather history: {e}")

# Function to retrieve search history from the database
def get_search_history():
    try:
        # Fetch all weather search history from the database
        history = WeatherSearchHistory.query.all()
        # Convert query results to dictionary format if necessary
        return [entry.to_dict() for entry in history]
    except Exception as e:
        print(f"Error fetching history: {e}")
        return []
