FROM ubuntu:18.04

COPY . ~/

WORKDIR ~

RUN apt-get update -y
RUN apt-get install -y python3 python3-pip
RUN python3 -m pip install -r ./manager_requirements.txt

ENTRYPOINT ["python3", "IRManager.py"]
