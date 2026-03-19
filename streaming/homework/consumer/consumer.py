import json

from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'green-trips',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    consumer_timeout_ms=5000,
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
)

count = 0

for message in consumer:
    trip = message.value
    if trip.get('trip_distance', 0) > 5.0:
        count += 1
    print(f"Trips with distance > 5.0 km: {count}", end='\r')

print(f"Trips with distance > 5.0 km: {count}")