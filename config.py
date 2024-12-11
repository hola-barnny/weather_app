import os

class Config:
    """Base configuration class with common settings."""
    SECRET_KEY = os.environ.get("SECRET_KEY", "b'\x86^\xed^X\xcf\xe7\x0e\x98\x93\xecY\x90\xfb\x05\xf3\x8a\xc0|\\\xbe\xe8=\x03'")
    WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY", "d9fea7939f24f617ce85b4327a724acc")
    DEBUG = os.environ.get("FLASK_DEBUG", "True") == "True"

class DevelopmentConfig(Config):
    """Development configuration."""
    FLASK_ENV = 'development'
    # Include the correct DATABASE_URI here
    DATABASE_URI = os.environ.get("DATABASE_URI", "mysql+pymysql://root:JasonZoe%401985@localhost:3306/weatherapp_db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    """Production configuration."""
    FLASK_ENV = 'production'
    # Include the correct DATABASE_URI here
    DATABASE_URI = os.environ.get("DATABASE_URI", "mysql+pymysql://root:JasonZoe%401985@localhost:3306/weatherapp_db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
