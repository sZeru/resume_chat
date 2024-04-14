# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 11:52:38 2024

@author: cdare
"""
from flask import Flask
from flask import render_template
from flask import request, jsonify
import pika

app = Flask(__name__)
@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/ask')
def ask():
    return render_template('ask.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.json.get('message')

    # Connect to RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare a queue
    channel.queue_declare(queue='rag1', durable=False)

    # Publish the message to the queue
    channel.basic_publish(exchange='', routing_key='rag1', body=message)
    print(" [x] Sent", message)

    # Close the connection
    connection.close()

    return jsonify({'status': 'Message sent to RabbitMQ'})

app.run(host="0.0.0.0", port=80)