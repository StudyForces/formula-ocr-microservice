FROM python:slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt update
RUN apt install -y libgl1-mesa-glx tesseract-ocr-rus

RUN pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu113
RUN pip3 install -r requirements.txt

COPY . .

CMD ["python", "-u", "/app/rmq_communication.py"]
