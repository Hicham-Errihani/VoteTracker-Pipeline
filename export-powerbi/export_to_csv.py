import json
import csv

with open("votes.json", encoding="utf-8") as f:
    data = json.load(f)

votes = [hit["_source"] for hit in data["hits"]["hits"]]

with open("votes.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["candidate", "party", "timestamp"])
    writer.writeheader()
    writer.writerows(votes)

print("✅ Fichier votes.csv généré avec succès.")
