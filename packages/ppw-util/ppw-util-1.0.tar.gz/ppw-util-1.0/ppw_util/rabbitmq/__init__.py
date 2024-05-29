# -*- coding: utf-8 -*
# #!/usr/bin/python3

# How to use: from ppw_util.rabbitmq import RabbitMQ
import pika
from pika.adapters.blocking_connection import BlockingChannel

class RabbitMQ:

    _conn: pika.BlockingConnection

    _channel: BlockingChannel

    def __init__(self, host: str, port: int, username: str, password: str):
        pika_credentials=pika.credentials.PlainCredentials(username, password)
        pika_conn_params = pika.ConnectionParameters(host=host, port=port, credentials=pika_credentials)
        self._conn = pika.BlockingConnection(pika_conn_params)
        self._channel = self._conn.channel()

    def publish_message(self, exchange: str, routing_key: str, body: str):
        self._channel.basic_publish(exchange = exchange, routing_key = routing_key, body = body) 


