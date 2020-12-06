from flask import request, Flask, render_template, jsonify
from werkzeug.utils import secure_filename
from collections import defaultdict
from threading import Lock
import requests
import json
import time
import os

mutex = Lock()

class IRManager:
    # job_id = 0
    worker_id = 0
    workers = defaultdict() # Store known workers. Key: worker id, Value: worker address
    # taskQueue = Queue() #queue that hold all requests for concurrency
    ava_worker = [] #available workers

    def __init__(self):
        root = os.path.dirname(__file__)
        self.img_folder = os.path.join(root, 'job-images')
        if not os.path.exists(self.img_folder):
            os.makedirs(self.img_folder)
    
    def processJob(self, filename):

        img = {'image': open('job-images/' + filename, 'rb')}

        while(True):
            if(len(self.ava_worker) == 0): 
                if(len(self.workers) == 0):
                    #no workers
                    print("No Workers!")
                    return "Service Error: No Processing Node!"
                # no usable worker
                print("No Available Worker Waiting")
                time.sleep(2)
                
                
            else:
                worker_id, ip = self.assignNext()
                # print(f"Try to Assign Job {self.job_id} to Worker {worker_id}")
                print(f"Try to Assign Job to Worker {worker_id}")
                if(self.checkAlive(worker_id, ip)):
                    print(f"Successfuly Assigned Job to Worker:{worker_id}")
                    r = requests.post(ip + "/predict", files=img)
                    self.ava_worker.append(worker_id)
                    return r.json()['result']
                else:
                    print(f"Failed to Assigned Job to Worker {worker_id}")

    def assignNext(self): # get id and address of the first worker in available workers

        worker_id = self.ava_worker[0]
        ip = self.workers[worker_id]
        del self.ava_worker[0]
        return worker_id, ip
    
    def checkAlive(self, id, ip): #check the status of a worker
        print(f"Checking Worker Status: {id} Address: {ip} ")
        try:
            r = requests.get(ip + "/status")
        except:
            print(f"Worker {id} Connect Failed")
            del self.workers[id]
            return False
        return r.status_code == 200

    def addworker(self, url):
        self.workers[self.worker_id] = url
        self.ava_worker.append(self.worker_id)
        print(f"Added Worker: {url} id:{self.worker_id}")
        self.worker_id+=1
        return True

    # def newjob(self):
    #     with mutex:
    #         tmp = self.job_id
    #         time.sleep(0.001)
    #         self.job_id = tmp + 1

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
    
        img = request.files['file']
        # Save the file

        newfilename = secure_filename("job-" + img.filename)
        img_path = os.path.join(manager.img_folder, newfilename)
        img.save(img_path)
        # print(f"saving file... id:{manager.job_id}")
        # manager.newjob()

        r = manager.processJob(newfilename)
        # print(f"Predict Result: {r.json()['result']}")
        print("Job Finished")
        return r


@app.route('/addnode', methods=['POST'])
def addnode():
    ip = request.remote_addr
    # print(request.form['port'])
    port = request.form['port']
    url = "http://" + ip + ":" + port
    if (manager.addworker(url)):
        return jsonify({'message': f"Worker Added Successfully"}), 200
    else:
        return jsonify({'message': "Worker Added Failed"}), 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5555", debug=True)