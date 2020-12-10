FROM ubuntu:18.04

COPY . ~/

WORKDIR ~

RUN apt-get update -y
RUN apt-get install -y python3 python3-pip
RUN python3 -m pip install torch==1.7.0+cpu torchvision==0.8.1+cpu torchaudio==0.7.0 -f https://download.pytorch.org/whl/torch_stable.html
RUN python3 -m pip install -r ./worker_requirements.txt
RUN python3 download_model.py

ENTRYPOINT ["python3", "worker.py"]
