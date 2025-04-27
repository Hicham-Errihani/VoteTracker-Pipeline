from flask import Flask, request, send_from_directory, jsonify
from kafka import KafkaProducer
from elasticsearch import Elasticsearch
import json
import time

app = Flask(__name__)

# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Elasticsearch Client
es = Elasticsearch("http://localhost:9200")

@app.route('/')
def serve_form():
    return send_from_directory('.', 'vote.html')

@app.route('/vote', methods=['POST'])
def vote():
    data = request.get_json()
    data['timestamp'] = time.time()
    producer.send('votes', value=data)
    return "Vote envoyé avec succès !"

@app.route('/last-votes')
def last_votes():
    res = es.search(index="votes", size=5, sort="timestamp:desc")
    votes = [hit["_source"] for hit in res["hits"]["hits"]]
    return jsonify(votes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

