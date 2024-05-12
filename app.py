# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 11:52:38 2024

@author: cdare
"""
from flask import Flask
from flask import render_template
from flask import request, jsonify
from flask_socketio import SocketIO, emit
import pika
import uuid
import base64
import json

class RpcClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, message, file_data):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        # Include file_data in the message body
        body = {'message': message, 'file_data': file_data}
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=json.dumps(body))  # Serialize body to JSON
        while self.response is None:
            self.connection.process_data_events(time_limit=None)
        return self.response


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='rpc_queue', durable=False)

client = RpcClient()

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/ask')
def ask():
    return render_template('ask.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form.get('message')  # Get the message from the form data
    file = request.files['file']  # Get the uploaded file

    # convert to base64
    file_data = base64.b64encode(file.read()).decode('utf-8')

    # Send the message and file data to the RPC function
    response = send_rpc_request(message, file_data)

    print(response.decode('utf-8'))
    return jsonify({'response': response.decode('utf-8')})

def send_rpc_request(message, file_data):
    response = client.call(message, file_data)
    return response

if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)