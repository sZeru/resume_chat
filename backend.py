import pika
import base64
import json
from rag import query

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='rpc_queue')


def on_request(ch, method, props, body):
    print(f" [X] Querying ({body})...")

    # Parse the body as JSON to extract message and file data
    request_data = json.loads(body.decode('utf-8'))
    message = request_data.get('message')
    file_data_base64 = request_data.get('file_data')  # Updated to match the key in the request

    # Decode base64-encoded file data
    file_data = base64.b64decode(file_data_base64)

    # Perform the query with the message and decoded PDF file data
    response = query(message, file_data)

    print(f" [X] Response: ({response})")

    # Publish the response
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id),
                     body=str(response)) 

    # Acknowledge the message
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)

print(" [x] Awaiting RPC requests")
channel.start_consuming()