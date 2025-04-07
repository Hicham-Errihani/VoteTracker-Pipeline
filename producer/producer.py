from kafka import KafkaProducer
import json
import time
import random

# Configuration du producteur Kafka
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Candidats et leurs partis politiques
candidates = {
    'HICHAM': 'Parti Alpha',
    'IKRAM': 'Parti Bêta',
    'SALIH': 'Parti Gamma'
}

# Envoi d’un vote toutes les 2 secondes
while True:
    candidate = random.choice(list(candidates.keys()))
    vote = {
        'candidate': candidate,
        'party': candidates[candidate],
        'timestamp': time.time()
    }
    producer.send('votes', vote)
    print(f"Vote envoyé : {vote}")
    time.sleep(2)

