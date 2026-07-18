from kafka import KafkaProducer
import json, time
producer = KafkaProducer(bootstrap_servers='kafka-headless:9092')
for i in range(10000):
  msg = {'email_id': i, 'sender': f'user{i}@example.com', 'content': 'Hello'}
  producer.send('raw-email', json.dumps(msg).encode())
  if i % 1000 == 0: print(f'Sent {i} emails')
producer.flush()
