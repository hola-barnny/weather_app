import os

class Config:
    """Base configuration class with common settings."""
    SECRET_KEY = os.environ.get("SECRET_KEY", "9c3b1ae7db8fd4617ca6317f7ef32bda969e2754ce220115430bcdb7a90bbbf0")
    WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY", "d9fea7939f24f617ce85b4327a724acc")
    DEBUG = os.environ.get("FLASK_DEBUG", "True").lower() in ["true", "1", "yes"]

    @staticmethod
    def check_environment_variable(variable_name, variable_value):
        """Warns if the environment variable is not set."""
        if variable_value is None:
            print(f"Warning: Using default value for {variable_name}. Set it in your environment for security.")

    # Check important variables
    check_environment_variable("SECRET_KEY", SECRET_KEY)
    check_environment_variable("WEATHER_API_KEY", WEATHER_API_KEY)


class DevelopmentConfig(Config):
    """Development configuration."""
    FLASK_ENV = 'development'
    DATABASE_URI = os.environ.get(
        "DATABASE_URI",
        "mysql+pymysql://dev_user:dev_password@localhost:3306/dev_weatherapp_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    """Production configuration."""
    FLASK_ENV = 'production'
    DATABASE_URI = os.environ.get(
        "DATABASE_URI",
        "mysql+pymysql://prod_user:prod_password@prod-db-server:3306/prod_weatherapp_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
