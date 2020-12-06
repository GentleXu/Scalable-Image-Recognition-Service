from flask import request, Flask, render_template, jsonify
from gevent.pywsgi import WSGIServer
from werkzeug.utils import secure_filename
import requests
import time
import os
from multiprocessing import Queue,Process
from collections import defaultdict
from time import sleep
BUSY = 0
IDLE = 1

class IRManager:
    job_id = 0
    worker_id = 0
    workers = defaultdict()
    status = [[],[]]
# taskQueue = Queue()

    def processJob(self, filename):

        my_img = {'image': open('images/' + filename, 'rb')}

        while(len(self.status[IDLE])>0):
            worker_id, ip = self.assignNext()
            print(f"assigned: {worker_id}")
            if(self.checkAlive(ip)):
                self.status[BUSY].append(worker_id)
                r = requests.post(ip + "/predict", files=my_img)
                self.status[BUSY].remove(worker_id)
                self.status[IDLE].append(worker_id)
                return r
       
        return "No worker to process"
        

    def assignNext(self):

        worker_id = self.status[IDLE][0]
        ip = self.workers[worker_id]
        del self.status[IDLE][0]
        return worker_id, ip
    
    def checkAlive(self, ip):
        print(ip)
        r = requests.get(ip + "/status")
        return r.status_code == 200

    def addworker(self, url):
        self.workers[self.worker_id] = url
        self.status[IDLE].append(self.worker_id)
        print(f"added worker: {url} id:{self.worker_id}")
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
        print("saving file...")

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

@app.route('/addnode', methods=['POST'])
def addnode():
    ip = request.remote_addr
    # print(request.form['port'])
    port = request.form['port']
    url = "http://" + ip + ":" + port
    if (manager.addworker(url)):
        return jsonify({'message': f"Worker {url} Added Successfully"}), 200
    else:
        return jsonify({'message': "Worker Added Failed"}), 400

if __name__ == '__main__':
    # http_server = WSGIServer(('0.0.0.0', 5555), app)
    # http_server.serve_forever() 
    app.run(host="0.0.0.0", port="5555", debug=True)