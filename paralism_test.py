import requests

import multiprocessing 
import time 
  
  
class Process(multiprocessing.Process): 
	def __init__(self, id, imgpath): 
		super(Process, self).__init__() 
		self.id = id
		self.imgpath = imgpath
				 
	def run(self):
		global global_start_time
		print("I'm the process with id: {}".format(self.id)) 
		start_time = time.time()
		r = requests.post(url, files={"file": open(self.imgpath, "rb")})
		print("process {} finished, used {} s, global time passed {} s".format(self.id, time.time() - start_time, time.time() - global_start_time))
		print(r)
  
url = "http://pcvm1-20.instageni.osu.edu:5555/predict"

base_path = "/Users/runqitian/Workspace/Fall2020/CS655/FinalProject/Scalable-Image-Recognition-Service/images/"
imgs = [base_path + "1.jpeg", base_path + "2.jpeg", base_path + "3.jpeg", base_path + "4.jpeg", base_path + "5.jpeg"]

global_start_time = time.time()
if __name__ == "__main__":
	ps = []
	for i in range(5):
		p = Process(i, imgs[i])
		ps.append(p)

	for p in ps:
		p.start()
