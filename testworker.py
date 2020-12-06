from __future__ import division, print_function
import os
import numpy as np
import requests
from PIL import Image
import torch.nn.functional as F
from torchvision import models, transforms
from werkzeug.utils import secure_filename
#from gevent.pywsgi import WSGIServer
from flask import request, Flask, render_template, jsonify
import time

status = "Alive"

app = Flask(__name__)
@app.route('/')
def home():
    return "This is a worker."

@app.route('/status', methods = ['GET'])
def getStatus():
    return status

@app.route('/predict', methods = ['POST'])
def predict():

    # get the image file
    f = request.files['image']

    time.sleep(30)

    print("Job Finished")

    return jsonify({'name': "test_name", 'result': f.filename})


if __name__ == "__main__":
    pt = input("Input Port Number: ")
    
    host = "http://0.0.0.0:5555"
    
    # poke the manager
    url = host + '/addnode'
    data = {"port": pt}
    r = requests.post(url, data)

    app.run(host="0.0.0.0", port=pt)
    #http_server = WSGIServer(('127.0.0.1', 5000), app)
    #http_server.serve_forever()
