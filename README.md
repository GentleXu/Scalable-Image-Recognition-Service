# Scalable Image Recognition Service
CS655 GENI mini project @BU
##Install Instruction
1. Clone or download this project from Github.
2. Use the Rspec file "rqtian_655_request_rspec.xml" to reserve resources on GENI and SSH to the Manager and Worker nodes.
3. On Manager machine, run `sudo docker run -t -p 80:80 runqi/cs655_vision_manager`
4. After the Manager machine is ready, on Worker machines, run `sudo docker run -t -p 6000:6000 --env MANAGER_HOST=<manager ip> runqi/cs655_vision_worker`, it would take about several minutes.
5. After the Worker machines receive acknowledgments from the Manager node, the user can visit `http://<manager public ip>`, it will display a web page for you to upload the image and show you the result.
6. In addition, you can use "parallelism_test.py" to test the system functionality. (remember to modify the url before testing)
