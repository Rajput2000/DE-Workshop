import json
import time

import pandas as pd
from kafka import KafkaProducer


url = "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-10.parquet"
columns = [
    'lpep_pickup_datetime', 'lpep_dropoff_datetime',
    'PULocationID', 'DOLocationID', 'passenger_count',
    'trip_distance', 'tip_amount', 'total_amount'
]
df = pd.read_parquet(url, columns=columns)

def row_serializer(row_dict):
    return json.dumps(row_dict).encode('utf-8')

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=row_serializer
)

topic_name = 'green-trips'
t0 = time.time()

for _, row in df.iterrows():
    record = row.to_dict()
    record['lpep_pickup_datetime'] = str(record['lpep_pickup_datetime'])
    record['lpep_dropoff_datetime'] = str(record['lpep_dropoff_datetime'])
    record['PULocationID'] = int(record['PULocationID'])
    record['DOLocationID'] = int(record['DOLocationID'])
    record['passenger_count'] = float(record['passenger_count'])
    record['trip_distance'] = float(record['trip_distance'])
    record['tip_amount'] = float(record['tip_amount'])
    record['total_amount'] = float(record['total_amount'])
    producer.send(topic_name, value=record)
    print(f"Sent record: {record}")
    # time.sleep(0.01)

producer.flush()
print(f'took {(time.time() - t0):.2f} seconds')
