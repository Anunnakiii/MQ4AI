"""
------------------------------------------------
    File Name:         MQ_Manager
    Author:            BoiWong
    Date:              2021/8/17
    Description:       消息队列模块, 负责 接收/发送 数据(使用RabbitMQ实现)
------------------------------------------------
"""

import pika


class MQ:
    def __init__(self, m_host, m_queue, m_routing_key):
        self.host = m_host
        self.queue = m_queue
        self.routing_key = m_routing_key

    def __send(self, m_body):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
        channel = connection.channel()
        channel.queue_declare(queue=self.queue)
        channel.basic_publish(exchange='', routing_key=self.routing_key, body=m_body)
        connection.close()

    def __rece(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
        channel = connection.channel()
        channel.queue_declare(queue=self.queue)

        def callback(ch, method, properties, body):
            print(f"Received {body}")
            # TODO   Save data/message to local file first or call Kitsune directly

        channel.basic_consume(queue=self.queue, on_message_callback=callback, auto_ack=True)
        channel.start_consuming()
