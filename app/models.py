from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import db

# Initialize the database
db = SQLAlchemy()

class WeatherSearchHistory(db.Model):
    __tablename__ = 'weather_search_history'
    
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    weather = db.Column(db.String(100), nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    icon = db.Column(db.String(50), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    date = db.Column(db.String(100), default=datetime.utcnow)
    
    def __repr__(self):
        return f"<WeatherSearchHistory {self.city} on {self.date}>"

    def to_dict(self):
        """ Convert model to dictionary for easy usage in templates or API responses. """
        return {
            'id': self.id,
            'city': self.city,
            'temperature': self.temperature,
            'weather': self.weather,
            'humidity': self.humidity,
            'icon': self.icon,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'date': self.date
        }

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)  # Last login timestamp

    def __repr__(self):
        return f"<User {self.username}>"

    def to_dict(self):
        """ Convert model to dictionary for easy usage in templates or API responses. """
        return {
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_joined': self.date_joined,
            'last_login': self.last_login
        }

class Settings(db.Model):
    __tablename__ = 'settings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    theme = db.Column(db.String(50), default='light')
    notifications_enabled = db.Column(db.Boolean, default=True)
    language = db.Column(db.String(50), default='en')

    user = db.relationship('User', backref=db.backref('settings', lazy=True))

    def __repr__(self):
        return f"<Settings for User {self.user_id}>"

    def to_dict(self):
        """ Convert model to dictionary for easy usage in templates or API responses. """
        return {
            'theme': self.theme,
            'notifications_enabled': self.notifications_enabled,
            'language': self.language
        }
