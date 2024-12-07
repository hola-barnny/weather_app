# app/weather_api.py
import requests
from config import Config

API_KEY = Config.WEATHER_API_KEY
BASE_URL = 'http://api.openweathermap.org/data/2.5/'

def get_weather(city):
    url = f"{BASE_URL}weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    if data['cod'] != 200:
        return None  # Handle errors if city not found or invalid
    return {
        'temperature': data['main']['temp'],
        'humidity': data['main']['humidity'],
        'weather': data['weather'][0]['description'],
        'icon': data['weather'][0]['icon']
    }

def get_forecast(city):
    url = f"{BASE_URL}forecast?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    forecast_data = response.json()
    if forecast_data['cod'] != '200':
        return None
    forecast_list = []
    for item in forecast_data['list']:
        forecast_list.append({
            'date': item['dt_txt'],
            'temperature': item['main']['temp'],
            'weather': item['weather'][0]['description'],
            'icon': item['weather'][0]['icon']
        })
    return forecast_list
