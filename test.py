import requests
from collections import defaultdict

if __name__ == '__main__':
    my_img = {'file': open('test.png', 'rb')}
    url = 'http://0.0.0.0:5555/predict'
    r = requests.post(url, files=my_img)
    print(r.json())
