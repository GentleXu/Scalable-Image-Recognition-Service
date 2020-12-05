import requests
from flask import request, Flask, jsonify
from time import sleep
def addnode(port):
    url = 'http://0.0.0.0:5555/addnode'
    data = {'port':port}
    r = requests.post(url, data=data)
    return r
# web servers
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    sleep(5000)

    return "Job Finished in 5000ms"

if __name__ == '__main__':
    # http_server = WSGIServer(('0.0.0.0', 11111), app)
    # http_server.serve_forever()
    pt = input("Enter your port [5000]") 
    print(addnode(pt).json())
    app.run(host="0.0.0.0", port=pt)
    