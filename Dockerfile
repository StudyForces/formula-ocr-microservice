FROM python:slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu
RUN pip3 install -r requirements.txt

COPY . .

CMD ["python", "-u", "/app/rmq_communication.py"]
