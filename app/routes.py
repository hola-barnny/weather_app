# app/routes.py
from flask import render_template, request
from app import app
from app.weather_api import get_weather, get_forecast

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/forecast', methods=['POST'])
def forecast():
    city = request.form['city']
    weather_data = get_weather(city)
    forecast_data = get_forecast(city)
    if weather_data is None:
        return render_template('index.html', error="City not found!")
    return render_template('forecast.html', weather=weather_data, forecast=forecast_data)

@app.route('/history', methods=['POST'])
def history():
    city = request.form['city']
    # Implement historical data feature here
    return render_template('history.html', history_data=history_data)

