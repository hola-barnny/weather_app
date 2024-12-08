# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask app
app = Flask(__name__)

# Load configuration from config.py
app.config.from_object('config.Config')

# Initialize the SQLAlchemy database object
db = SQLAlchemy(app)

# Import routes after initializing the app and db
from app import routes
