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
    job_id = 0
    worker_id = 0
    workers = defaultdict() # Store known workers. Key: worker id, Value: worker address
    # taskQueue = Queue() #queue that hold all requests for concurrency
    ava_worker = [] #available workers

    def __init__(self):
        root = os.path.dirname(__file__)
        self.img_folder = os.path.join(root, 'job-images')
        if not os.path.exists(self.img_folder):
            os.makedirs(self.img_folder)
    
    def processJob(self, filename, jid):

        img = {'image': open('job-images/' + filename, 'rb')}

        while(True):
            if(len(self.ava_worker) == 0): 
                if(len(self.workers) == 0):
                    #no workers
                    print("No Workers!")
                    return "Service Error: No Processing Node!", 404
                # no usable worker
                # print("No Available Worker, Waiting")
                time.sleep(2)
            
            else:
                worker_id, ip = self.assignNext()
                print(f"Try to Assign Job {jid} to Worker {worker_id}")

                if(self.checkAlive(worker_id)):
                    print(f"Successfuly Assigned Job: {jid} to Worker:{worker_id}")
                    try:
                        r = requests.post(ip + "/predict", files=img)
                    except:
                        # worker failed during processing, reassign job
                        print(f"Worker {worker_id} Connect Failed, Re-Assign Job {jid}")
                        self.removeworker(worker_id)
                        continue                   
 
                    self.ava_worker.append(worker_id)
                    return r.json()['result'], 200
                else:
                    print(f"Failed to Assigned Job {jid} to Worker {worker_id}")

    def assignNext(self): # get id and address of the first worker in available workers

        worker_id = self.ava_worker[0]
        ip = self.workers[worker_id]
        del self.ava_worker[0]
        return worker_id, ip
    
    def checkAlive(self, wid): #check status of a worker
        print(f"Checking Worker {wid} Status")
        try:
            r = requests.get(self.workers[wid] + "/status")
        except:
            print(f"Worker {wid} Connect Failed")
            self.removeworker(wid)
            return False
        if (r.status_code == 200):
            return True
        else:
            self.removeworker(wid)
            return False

    def addworker(self, url):
        with mutex:
            wid = self.worker_id
            time.sleep(0.001)
            self.worker_id+=1
            self.workers[wid] = url
            self.ava_worker.append(wid)

        print(f"Added Worker {wid} address: {url}")

        return True

    def removeworker(self, wid):
        del self.workers[wid]
        print(f"Removed Worker {wid}")

    def newjob(self):
        with mutex:
            jid = self.job_id
            time.sleep(0.001)
            self.job_id+=1
            return jid
            

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
        # get job id
        jobid = manager.newjob()
        # get file
        img = request.files['file']
        # save the file
        newfilename = secure_filename("job-" + str(jobid) + "-" + img.filename)
        img_path = os.path.join(manager.img_folder, newfilename)
        img.save(img_path)
        print(f"Saving File... id: {jobid}")

        r, c = manager.processJob(newfilename, jobid)
        # print(f"Predict Result: {r.json()['result']}")
        if(c==200):
            print(f"Job {jobid} Finished")
        
        return r


@app.route('/addnode', methods=['POST'])
def addnode():
    ip = request.remote_addr
    # print(request.form['port'])
    port = request.form['port']
    url = "http://" + ip + ":" + port
    if (manager.addworker(url)):
        return jsonify({'message': "Worker Added Successfully"})
    else:
        return jsonify({'message': "Worker Added Failed"}), 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="80")