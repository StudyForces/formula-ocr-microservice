# Formula-OCR-Microservice

Service that can recognize formulas from images

## Requirements
- [requirements](https://github.com/StudyForces/formula-ocr-microservice/blob/7eca4763e7941d8737cca3a3aa295aae554735d9/requirements.txt)

## Usage
All images must be in .png format.

Set the required parameters in the environment variables

- SENDER_QUEUE_NAME - name of the queue to be used as output
- CONSUMER_QUEUE_NAME - name of the queue to be used as input
- HOST - URL for connecting to RabbitMQ

Then run the following command

	python rmq_communication.py
