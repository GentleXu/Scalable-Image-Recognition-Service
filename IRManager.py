from flask import request, Flask, render_template, jsonify
from gevent.pywsgi import WSGIServer
from werkzeug.utils import secure_filename
import requests
import time
import os
from multiprocessing import Queue,Process

BUSY = 0
IDLE = 1

class IRManager:
    job_id = 0
    worker_id = 0
    workers = {}
    status = [[],[]]
# taskQueue = Queue()

    def processJob(self, filename):
        id = self.status[IDLE][0]
        self.status[BUSY].append(id)
        ip = self.workers[id]
        del self.status[IDLE][0]
        my_img = {'image': open('images/' + filename, 'rb')}
        url = "http://" + ip + ":5000/predict"
            
        return requests.post(url, files=my_img)

    
    def addworker(self, ip):
        self.workers[self.worker_id] = ip
        self.status[IDLE].append(self.worker_id)
        self.worker_id+=1
        return True

# web servers
app = Flask(__name__)
manager = IRManager()
@app.route('/', methods=['GET'])
def index():
    # Main page
    page = ""
    with open("index.html", "r") as rf:
        for line in rf.readlines():
            page += line + "\n"
    return page


@app.route('/predict', methods=['POST'])
def upload():
        print("begian predict")
        # Receive the file
        start_time = time.time()

        img = request.files['file']
        # Save the file
        root = os.path.dirname(__file__)
        img_folder = os.path.join(root, 'images')
        if not os.path.exists(img_folder):
            os.makedirs(img_folder)
        img.filename = str(manager.job_id) +"-"+ img.filename
        img_path = os.path.join(img_folder, secure_filename(img.filename))
        img.save(img_path)
        manager.job_id+=1
        r = manager.processJob(img.filename)
        # print(r.json()['result'])
        return r.json()['result']
        
        # return jsonify({'message': "No Idle Worker"}), 417
        # return jsonify({'message': "get & save image", 'file': img.filename}), 200
        # my_img = {'name': "image1", 'image': f}
        # r = requests.post(url, files=my_img)

@app.route('/addnode', methods=['GET'])
def addnode():
    ip = request.remote_addr

    if (manager.addworker(ip)):
        return jsonify({'message': f"Worker {ip} Added Successfully: \n{manager.workers}"}), 200
    else:
        return jsonify({'message': "Worker Added Failed"}), 417

if __name__ == '__main__':
    # http_server = WSGIServer(('0.0.0.0', 5555), app)
    # http_server.serve_forever() 
    app.run(host="0.0.0.0", port="5555", debug=True)