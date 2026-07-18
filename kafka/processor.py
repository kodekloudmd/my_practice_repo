from kafka import KafkaConsumer, KafkaProducer
import json, time
consumer = KafkaConsumer('raw-email', bootstrap_servers='kafka-headless:9092', group_id='scanner-group')
producer = KafkaProducer(bootstrap_servers='kafka-headless:9092')
for msg in consumer:
  data = json.loads(msg.value.decode())
  time.sleep(0.1) # simulate scan
  data['verdict'] = 'clean' if data['email_id'] % 5 != 0 else 'malicious'
  producer.send('enriched-email', json.dumps(data).encode())
