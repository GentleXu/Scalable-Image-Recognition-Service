import requests

import multiprocessing 
import time 
  
  
class Process(multiprocessing.Process): 
    def __init__(self, id, imgpath): 
        super(Process, self).__init__() 
        self.id = id
        self.imgpath = imgpath
                 
    def run(self): 
        print("I'm the process with id: {}".format(self.id)) 
        r = requests.post(url, files={"file": open(self.imgpath, "rb")})
        print("process {} finished".format(self.id))
        print(r)
  
# if __name__ == '__main__': 
#     p = Process(0) 
#     p.start() 
#     p.join() 
#     p = Process(1) 
#     p.start() 
#     p.join()

url = "http://pcvm1-20.instageni.osu.edu:5555/predict"

base_path = "/Users/runqitian/Workspace/Fall2020/CS655/FinalProject/"
imgs = [base_path + "img1.jpg", base_path + "img2.png", base_path + "img3.jpg", base_path + "img4.jpeg", base_path + "img5.jpg"]

if __name__ == "__main__":
	ps = []
	for i in range(5):
		p = Process(i, imgs[i])
		ps.append(p)

	for p in ps:
		p.start()
	time.sleep(20)
	# ps[0].join()
# for p in ps:
# 	p.start()