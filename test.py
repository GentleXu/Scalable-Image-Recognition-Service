import requests
if __name__ == '__main__':
    my_img = {'file': open('test.png', 'rb')}
    url = 'http://0.0.0.0:5555/addnode'
    r = requests.post(url, files=my_img)
    print(r.json())
