# amqps://zjqmyjmm:f1m1faiP_38J8j7JoOFGKQs-R2wmkKnW@collie.lmq.cloudamqp.com/zjqmyjmm

import pika, json

params = pika.URLParameters('amqps://zjqmyjmm:f1m1faiP_38J8j7JoOFGKQs-R2wmkKnW@collie.lmq.cloudamqp.com/zjqmyjmm')

connection = pika.BlockingConnection(params)
channel = connection.channel()

def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='admin', body=json.dumps(body), properties=properties)

    