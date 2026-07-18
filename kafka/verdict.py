from kafka import KafkaConsumer
import json
consumer = KafkaConsumer('enriched-email', bootstrap_servers='kafka-headless:9092', group_id='verdict-group')
for msg in consumer:
  data = json.loads(msg.value.decode())
  print(f"Email {data['email_id']} → {data['verdict']}")
