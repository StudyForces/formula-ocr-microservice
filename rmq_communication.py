import os
import pika
import json
import requests
import utils
from PIL import Image
from OCR import get_latex
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("HOST")
SENDER_QUEUE_NAME = os.getenv("SENDER_QUEUE_NAME")
CONSUMER_QUEUE_NAME = os.getenv("CONSUMER_QUEUE_NAME")

connection = pika.BlockingConnection(pika.ConnectionParameters(HOST))

rmq_channel = connection.channel()
session = requests.Session()

rmq_channel.exchange_declare(exchange=SENDER_QUEUE_NAME, exchange_type='topic', durable=True)


def send(message: str) -> None:
    rmq_channel.basic_publish(exchange=SENDER_QUEUE_NAME, routing_key=SENDER_QUEUE_NAME, body=message)


def on_message(channel, method_frame, header_frame, body) -> None:
    rmq_channel.basic_ack(method_frame.delivery_tag)
    data = json.loads(body)
    print(data)
    if not utils.download_image(session, data["url"], "temp.png"):
        return None
    rect = data["rect"]
    data.pop("rect")
    data.pop("url")
    data.update([("data", dict().fromkeys(["latex"], [""]))])
    data["data"]["latex"] = get_latex(Image.open("temp.png").crop((int(rect["x"]), int(rect["y"]),
                                                                   int(rect["width"]), int(rect["height"]))))
    send(json.dumps(data, separators=(',', ':'), ensure_ascii=False))


result = rmq_channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

rmq_channel.queue_bind(exchange=CONSUMER_QUEUE_NAME, queue=queue_name, routing_key=CONSUMER_QUEUE_NAME)

rmq_channel.basic_consume(
    queue=queue_name, on_message_callback=on_message, auto_ack=False)

try:
    rmq_channel.start_consuming()
except KeyboardInterrupt:
    rmq_channel.close()
    session.close()
