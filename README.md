# rag_hackathon

Hackathon project for CMPE 172, Spring 2024.

## Dependencies
- Python
- npm
- RabbitMQ
- Erlang
- Ollama

### Run these commands in your terminal first (May be different depending on your system)
- pip install llama-index
- pip install llama-index-llms-ollama
- pip install llama-index-embeddings-huggingface
- python -m pip install pika --upgrade
- npm install amqplib
- pip install flask-socketio

### Install the following programs
- Ollama (https://github.com/ollama/ollama). Afterwards, run 'ollama pull mistral` in the terminal
- RabbitMQ (https://www.rabbitmq.com/).

### To run the program
- open Ollama
- start the RabbitMQ service
- run app.py
- run backend.py
- Access the website on your local address (http://127.0.0.1:5000)
