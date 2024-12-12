import os

class Config:
    """Base configuration class with common settings."""
    
    # Environment variables with fallback for critical ones, but warn if not set
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key_for_dev") 
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "default_weather_api_key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Database URI (use defaults for local dev environment)
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URI", "mysql+pymysql://root:password@localhost:3306/weatherapp_db"
    )

    @staticmethod
    def check_environment_variable(variable_name):
        """Warns if the environment variable is not set."""
        variable_value = os.getenv(variable_name)
        if not variable_value:
            print(f"Warning: {variable_name} not set. Please set it in your environment for security.")
        return variable_value

    # Check critical environment variables
    check_environment_variable("SECRET_KEY")
    check_environment_variable("WEATHER_API_KEY")
    check_environment_variable("DATABASE_URI")


class DevelopmentConfig(Config):
    """Development configuration."""
    FLASK_ENV = 'development'
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URI", 
        "mysql+pymysql://dev_user:dev_password@localhost:3306/dev_weatherapp_db"
    )

class ProductionConfig(Config):
    """Production configuration."""
    FLASK_ENV = 'production'
    DEBUG = False

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URI",
        "mysql+pymysql://prod_user:prod_password@prod-db-server:3306/prod_weatherapp_db"
    )
