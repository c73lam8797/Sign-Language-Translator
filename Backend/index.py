import os
import tensorflow as tf
from tensorflow import keras
from flask import Flask, jsonify, request
from flask_cors import CORS
app = Flask(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})

model = keras.models.load_models("../Models/")

@app.route('/')
def index():
    return "Hello World!"

@app.route('/api/predict', methods=["POST"])
def predict_img():
    try:
        img = request.get_json(force=True)
    except HTTPException as e:
        return jsonify({'error': 'Request data invalid'}), 400


if __name__ == '__main__':
   app.run()