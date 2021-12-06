try:
    import pika
    import ast
    import json

except Exception as e:
    print('Some moduls are missing {}'.format(e))



# def sender(body):
#     connection = pika.BlockingConnection(
#     pika.ConnectionParameters('localhost', heartbeat=600, blocked_connection_timeout=300))
#
#     channel = connection.channel()
#     channel.queue_declare(queue='sendData')
#     channel.basic_publish(exchange='', routing_key='sendData', body=json.dumps(body), properties=pika.BasicProperties(delivery_mode=2))
#     print('information hs been sent')
#     connection.close()


def sender(body):
    credentials = pika.PlainCredentials(username='bogi', password='bogi')
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq', heartbeat=600, blocked_connection_timeout=300, credentials=credentials))
    channel = connection.channel()
    channel.exchange_declare(exchange='logs', exchange_type='fanout')

    channel.basic_publish(exchange='logs', routing_key='', body=json.dumps(body))
    print(" [x] Sent %r" % body)
    connection.close()




import uuid

class CheckIfDefenderExist(object):

    def __init__(self):
        self.credentials = pika.PlainCredentials(username='bogi', password='bogi')
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='rabbitmq', heartbeat=600, blocked_connection_timeout=300, credentials=self.credentials))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=json.dumps(n))
        while self.response is None:
            self.connection.process_data_events()
        return self.response