import os

class Config:
    """Base configuration class with common settings."""
    SECRET_KEY = os.environ.get("SECRET_KEY", "your_default_secret_key")  # Secret key for session management
    WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY", "your_openweathermap_api_key")  # API key for OpenWeatherMap
    DEBUG = os.environ.get("FLASK_DEBUG", "True") == "True"  # Enable or disable debug mode

class DevelopmentConfig(Config):
    """Development configuration."""
    FLASK_ENV = 'development'  # Set the environment to 'development'
    DATABASE_URI = os.environ.get("DATABASE_URI", "mysql+pymysql://root:your_password@localhost/weatherapp_db")  # MySQL URI for dev
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable Flask-SQLAlchemy modification tracking for performance reasons

class ProductionConfig(Config):
    """Production configuration."""
    FLASK_ENV = 'production'  # Set the environment to 'production'
    DATABASE_URI = os.environ.get("DATABASE_URI", "mysql+pymysql://root:your_password@localhost/weatherapp_db")  # MySQL URI for prod
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable Flask-SQLAlchemy modification tracking
    DEBUG = False  # Disable debug mode in production
