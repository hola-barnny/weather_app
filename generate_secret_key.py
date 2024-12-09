from flask import Flask
import os

app = Flask(__name__)

# Set a random SECRET_KEY
app.secret_key = os.urandom(24)  # This will generate a 24-byte random key

print(app.secret_key)  # Print to verify the key
