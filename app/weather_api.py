import requests
from config import Config
import logging

# Fetch API key from config
API_KEY = Config.WEATHER_API_KEY
BASE_URL = 'http://api.openweathermap.org/data/2.5/'

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_weather_data_by_city(city):
    """
    Fetches the current weather data for a city from OpenWeatherMap using city name.
    :param city: Name of the city to fetch the weather for.
    :return: A dictionary containing weather details or an error message.
    """
    url = f"{BASE_URL}weather?q={city}&appid={API_KEY}&units=metric"  # Corrected URL formatting
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data.get('cod') != 200:
            logger.error(f"Failed to fetch weather data: {data.get('message')}")
            return {"error": data.get("message", "Unknown error occurred.")}

        return {
            'city': data['name'],
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'weather': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon'],
            'latitude': data['coord']['lat'],
            'longitude': data['coord']['lon']
        }
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching weather data: {e}")
        return {"error": "Unable to fetch weather data at this time."}

def get_forecast_data(city):
    """
    Fetches the 5-day weather forecast data for a city from OpenWeatherMap using city name.
    :param city: Name of the city to fetch the forecast for.
    :return: A list of forecast dictionaries or an error message.
    """
    url = f"{BASE_URL}forecast?q={city}&appid={API_KEY}&units=metric"  # Corrected URL formatting
    try:
        response = requests.get(url)
        response.raise_for_status()
        forecast_data = response.json()

        if forecast_data.get('cod') != '200':
            logger.error(f"Failed to fetch forecast data: {forecast_data.get('message')}")
            return {"error": forecast_data.get("message", "Unknown error occurred.")}

        # Prepare the forecast list with the necessary data
        forecast_list = [
            {
                'date': item['dt_txt'],
                'temperature': item['main']['temp'],
                'weather': item['weather'][0]['description'],
                'icon': item['weather'][0]['icon']
            }
            for item in forecast_data['list']
        ]
        return forecast_list
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching forecast data: {e}")
        return {"error": "Unable to fetch forecast data at this time."}
