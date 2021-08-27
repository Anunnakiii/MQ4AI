"""
------------------------------------------------
    File Name:         MQ_Manager
    Author:            BoiWong
    Date:              2021/8/17
    Description:       消息队列模块, 负责 接收/发送 数据(使用RabbitMQ实现)
------------------------------------------------
"""
import json
import pika


class MQ:
    def __init__(self, m_host, m_port, m_user, m_password, m_queue, m_routing_key, m_exchange=""):
        self.host = m_host
        self.port = m_port
        self.user = m_user
        self.password = m_password
        self.exchange = m_exchange
        self.queue = m_queue
        self.routing_key = m_routing_key
        self.is_connected = False
        try:
            credentials = pika.PlainCredentials(self.user, self.password)  # 身份认证
            connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=self.host, port=self.port, credentials=credentials))
            self.channel = connection.channel()
            self.channel.queue_declare(queue=self.queue, durable=True)
            self.is_connected = True
        except Exception as e:
            print(e)
            exit(1)

    def callback(self, ch, method, properties, body):
        print(f"Received: {body.decode()}")
        # data = json.loads(body)
        # print(type(data), data)
        # TODO   Save data/message to local file first or call Kitsune directly

    def send(self, m_body):
        if self.is_connected:
            print(f"Message Sent: {m_body}")
            self.channel.basic_publish(exchange=self.exchange, routing_key=self.routing_key, body=m_body,
                                       properties=pika.BasicProperties(delivery_mode=2, ))

    def rece(self):
        if self.is_connected:
            self.channel.basic_consume(queue="ai", on_message_callback=self.callback, auto_ack=True)
            self.channel.start_consuming()
