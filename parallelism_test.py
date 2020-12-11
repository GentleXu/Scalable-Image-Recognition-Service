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
		# global url
		print("I'm the process with id: {}".format(self.id))
		start_time = time.time()
		r = requests.post(url, files={"file": open(self.imgpath, "rb")})
		print("process {} finished, used {} s, global time passed {} s".format(self.id, time.time() - start_time, time.time() - global_start_time))
		print(r.content)
		# print(r.)

# url = "http://pc vm1-4.geni.case.edu/predict"

url = "http://0.0.0.0/predict"

base_path = "test/"
imgs = [base_path + "test0.jpg", base_path + "test1.jpg", base_path + "test2.jpg", base_path + "test3.jpg", base_path + "test4.jpg"]

global_start_time = time.time()
if __name__ == "__main__":
	ps = []
	for i in range(30):
		p = Process(i, imgs[i%5])
		ps.append(p)

	for p in ps:
		p.start()
