from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, DoubleType

# Création de la session Spark
spark = SparkSession.builder \
    .appName("KafkaToElastic") \
    .config("spark.es.nodes", "localhost") \
    .config("spark.es.port", "9200") \
    .config("spark.es.nodes.wan.only", "true") \
    .getOrCreate()

# Schéma des données Kafka
schema = StructType() \
    .add("candidate", StringType()) \
    .add("party", StringType()) \
    .add("timestamp", DoubleType())

# Lecture des messages Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "votes") \
    .option("startingOffsets", "latest") \
    .load()

# Conversion du message Kafka JSON en colonnes
json_df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# Écriture dans Elasticsearch
es_query = json_df.writeStream \
    .format("org.elasticsearch.spark.sql") \
    .option("checkpointLocation", "/tmp/spark-checkpoint") \
    .option("es.resource", "votes") \
    .start()

# Affichage en console pour voir les messages en temps réel
console_query = json_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", False) \
    .start()

# Attente de fin des deux streams
es_query.awaitTermination()
console_query.awaitTermination()

