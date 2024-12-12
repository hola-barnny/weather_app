import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
        """
        Logs a warning if the environment variable is not set.
        :param variable_name: Name of the environment variable.
        :return: Value of the environment variable or None.
        """
        variable_value = os.getenv(variable_name)
        if not variable_value:
            logger.warning(f"Environment variable {variable_name} is not set.")
        return variable_value

    # Check critical environment variables
    @classmethod
    def validate_critical_env_vars(cls):
        """Validates critical environment variables and logs warnings if unset."""
        cls.check_environment_variable("SECRET_KEY")
        cls.check_environment_variable("WEATHER_API_KEY")
        cls.check_environment_variable("DATABASE_URI")


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


def get_config():
    """
    Returns the appropriate configuration class based on the NODE_ENV environment variable.
    Defaults to DevelopmentConfig if NODE_ENV is not set or invalid.
    :return: Configuration class.
    """
    env = os.getenv("NODE_ENV", "development").lower()
    if env == "production":
        logger.info("Using ProductionConfig.")
        return ProductionConfig
    logger.info("Using DevelopmentConfig.")
    return DevelopmentConfig


# Validate critical environment variables at module load
Config.validate_critical_env_vars()
