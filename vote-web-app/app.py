from flask import Flask, request, send_from_directory
from kafka import KafkaProducer
import json
import time

app = Flask(__name__)

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

@app.route('/')
def serve_form():
    return send_from_directory('.', 'vote.html')

@app.route('/vote', methods=['POST'])
def vote():
    data = request.get_json()
    data['timestamp'] = time.time()
    producer.send('votes', value=data)
    return "Vote envoyé avec succès !"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
