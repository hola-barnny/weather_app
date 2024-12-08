from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Initialize extensions
db = SQLAlchemy()

def create_app():
    # Load environment variables from a .env file
    load_dotenv()

    # Create Flask app instance
    app = Flask(__name__)

    # App configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions with the app
    db.init_app(app)

    # Register blueprints or routes
    from app.routes import main  # Import blueprint or routes
    app.register_blueprint(main)

    # Create database tables (optional for development)
    with app.app_context():
        db.create_all()

    return app
