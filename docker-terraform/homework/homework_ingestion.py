import pandas as pd
from sqlalchemy import create_engine
import click

@click.command()
@click.option('--user', default='root', help='PostgreSQL user')
@click.option('--password', default='root', help='PostgreSQL password')
@click.option('--host', default='localhost', help='PostgreSQL host')
@click.option('--port', default=5432, type=int, help='PostgreSQL port')
@click.option('--db', default='ny_taxi', help='PostgreSQL database name')
def ingest_data(user, password, host, port, db):
    # Load green taxi trip data
    green_taxi_trips_url = 'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet'

    dtype = {
        "VendorID": "Int64",
        "passenger_count": "Int64",
        "trip_distance": "float64",
        "RatecodeID": "Int64",
        "store_and_fwd_flag": "string",
        "PULocationID": "Int64",
        "DOLocationID": "Int64",
        "payment_type": "Int64",
        "fare_amount": "float64",
        "extra": "float64",
        "mta_tax": "float64",
        "tip_amount": "float64",
        "tolls_amount": "float64",
        "improvement_surcharge": "float64",
        "total_amount": "float64",
        "congestion_surcharge": "float64",
        "trip_type": "Int64",
        "cbd_congestion_fee": "float64",
        "lpep_pickup_datetime": "datetime64[ns]",
        "lpep_dropoff_datetime": "datetime64[ns]"
    }

    print("Loading green taxi trips data...")
    df = pd.read_parquet(green_taxi_trips_url)
    print(f"Loaded {len(df)} rows")

    # Adjust data types
    print("Adjusting data types...")
    green_taxi_trips_df = df.astype(dtype=dtype)
    print("Data types adjusted")

    # Load taxi zone lookup data
    print("\nLoading taxi zone lookup data...")
    zones_url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv"
    zone_df = pd.read_csv(zones_url)
    print(f"Loaded {len(zone_df)} zones")

    # Create database engine
    print("\nConnecting to database...")
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    print("Connected to database")

    print("\nUploading green taxi trips to database...")
    green_taxi_trips_df.to_sql(name='green_taxi_trips', con=engine, if_exists='replace', index=False)
    print("Green taxi trips uploaded successfully")

    print("\nUploading taxi zones to database...")
    zone_df.to_sql(name='taxi_zones', con=engine, if_exists='replace', index=False)
    print("Taxi zones uploaded successfully")

    print("\nAll data uploaded successfully!")

if __name__ == '__main__':
    ingest_data()