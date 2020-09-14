import os
import tensorflow as tf
from tensorflow import keras
from flask import Flask, jsonify, request
from flask_cors import CORS
import io, base64
import numpy as np
import cv2
from io import BytesIO
from PIL import Image
from binascii import a2b_base64
app = Flask(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})

model = keras.models.load_model("../Models/CNN1.h5")

@app.route('/')
def index():
    return "Hello World!"

@app.route('/api/predict', methods=["POST"])
def predict_img():
    content = request.form['b64']
    content = content.replace('data:image/png;base64,', '')

    HEIGHT = WIDTH = 180

    img = Image.open(BytesIO(base64.b64decode(content + '==='))).convert('RGB')
    img = img.resize((WIDTH, HEIGHT))
    img  = np.array(img)/255


    img_array = tf.expand_dims(img, 0) # Create a batch

    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])

    class_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'del', 'nothing', 'space']

    return jsonify(classification=class_names[np.argmax(score)], confidence=100 * np.max(score))



if __name__ == '__main__':
   app.run()
