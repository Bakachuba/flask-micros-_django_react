import json

import pika

params = pika.URLParameters('amqps://mmztoxid:TQVZqXcDQ_flhn9wAFD0WtxsnSfjiF1Q@hawk.rmq.cloudamqp.com/mmztoxid')

connection = pika.BlockingConnection(params)

channel = connection.channel()

def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='admin', body=json.dumps(body), properties=properties)
