from flask import Flask, request, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from functools import wraps
from dotenv import load_dotenv
import os

# create the application object
app = Flask(__name__)

# enable CORS
CORS(app)

# config
load_dotenv()
app.config.from_object(os.environ['APP_SETTINGS'])

# create db object
db = SQLAlchemy(app)

# import db schema
from models import Room, Player

# routes
@app.route('/')
def home():
    return "Welcome to LambdaQuest2: Coin Miner"


@app.route('/api')
def api_status():
    response = {"status": "up"}
    return jsonify(response), 200


@app.route('/api/rooms')
def rooms_api():
    if request.method == 'GET':
        try:
            response = db.session.query(Room).all()
            print(response)
        except:
            flash('Missing the DB!')
        return "Getting rooms"


if __name__ == '__main__':
    app.run()

