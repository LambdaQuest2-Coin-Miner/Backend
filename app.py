from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from dotenv import load_dotenv
import os

# create the application object
app = Flask(__name__)

# config
load_dotenv()
app.config.from_object(os.environ['APP_SETTINGS'])

# create db object
db = SQLAlchemy(app)

# import db schema
from models import *

# routes
@app.route('/')
def home():
    return "Welcome to LambdaQuest2: Coin Miner"

if __name__ == '__main__':
    app.run()

