import os


class Config:
    """Base configuration class with common settings."""

    # Load environment variables with fallback values
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key_for_dev")
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "default_weather_api_key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Database URI (fallback to a local dev environment)
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URI", "mysql+pymysql://root:password@localhost:3306/weatherapp_db"
    )

    @staticmethod
    def check_environment_variable(variable_name):
        """Warns if the environment variable is not set."""
        variable_value = os.getenv(variable_name)
        if not variable_value:
            print(f"Warning: {variable_name} is not set. Please set it in your environment for security.")
        return variable_value

    # Check critical environment variables
    check_environment_variable("SECRET_KEY")
    check_environment_variable("WEATHER_API_KEY")
    check_environment_variable("DATABASE_URI")


class DevelopmentConfig(Config):
    """Development configuration."""
    FLASK_ENV = 'development'
    DEBUG = True

    # Overwrite the database URI for development if available
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URI", "mysql+pymysql://root:password@localhost:3306/dev_weatherapp_db"
    )


class ProductionConfig(Config):
    """Production configuration."""
    FLASK_ENV = 'production'
    DEBUG = False

    # Overwrite the database URI for production if available
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URI", "mysql+pymysql://root:password@prod-db-server:3306/prod_weatherapp_db"
    )


# Choose the correct configuration based on the environment
def get_config():
    """Returns the appropriate configuration class based on NODE_ENV."""
    env = os.getenv("NODE_ENV", "development").lower()
    if env == "production":
        return ProductionConfig
    return DevelopmentConfig
