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
    def __init__(self, m_host, m_port, m_user, m_password, m_queue, m_routing_key, m_exchange, m_r_exchange,
                 m_r_queue):
        self.host = m_host
        self.port = m_port
        self.user = m_user
        self.password = m_password
        self.exchange = m_exchange
        self.r_exchange = m_r_exchange
        self.queue = m_queue
        self.r_queue = m_r_queue
        self.routing_key = m_routing_key
        self.is_connected = False
        self.obj = None
        try:
            credentials = pika.PlainCredentials(self.user, self.password)  # 身份认证
            connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=self.host, port=self.port, credentials=credentials))
            self.channel = connection.channel()
            self.r_channel = connection.channel()
            self.channel.queue_declare(queue=self.queue, durable=True)
            self.r_channel.queue_declare(queue=self.r_queue, durable=True)
            self.is_connected = True
        except Exception as e:
            print(e)
            exit(1)

    def callback(self, ch, method, properties, body):
        print(f"From: {self.r_queue} Received: {body.decode()}")
        self.send(b'{"rev":1}')

        # data = json.loads(body)
        # print(type(data), data)
        # TODO   Save data/message to local file first or call Kitsune directly

    def send(self, m_body):
        if self.is_connected:
            print(f"Send to: {self.queue} Message : {m_body}")
            self.channel.basic_publish(exchange=self.exchange, routing_key=self.routing_key,
                                       body=m_body,
                                       properties=pika.BasicProperties(delivery_mode=2, ))

    def rece(self, rec_queue=None, m_obj=None):
        if m_obj is not None:
            self.obj = m_obj
        if self.r_queue is None:
            self.r_queue = rec_queue
        if self.is_connected and self.r_queue is not None:
            self.r_channel.basic_consume(queue=self.r_queue, on_message_callback=self.callback, auto_ack=True)
            self.r_channel.start_consuming()
