import pika
import signal
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
count = 0

def callback(ch, method, properties, body):
     global count
     count += 1
     print(" [x] Received %r" % body)

def signal_handler(sig, frame):
    print("\nMessages received:", count)
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
channel.basic_consume(queue='rag1',auto_ack=True,on_message_callback=callback)
print(' [*] Waiting for messages. To exit press CTRL+C\n')
channel.start_consuming()