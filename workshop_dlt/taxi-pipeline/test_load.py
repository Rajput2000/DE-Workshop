#!/usr/bin/env python3
"""Simple test to verify dlt can load REST API data."""

import dlt
from dlt.sources.rest_api import rest_api_source

# Configure the REST API source
config = {
    "client": {
        "base_url": "https://us-central1-dlthub-analytics.cloudfunctions.net",
    },
    "resources": [
        {
            "name": "taxi_data",
            "endpoint": {
                "path": "/data_engineering_zoomcamp_api",
                "paginator": {
                    "type": "page_number",
                    "page_param": "page",
                    "base_page": 1,
                    "stop_after_empty_page": True,
                },
                "params": {
                    "limit": 1000,
                },
            },
        },
    ],
}

# Create source
source = rest_api_source(config)

# Create pipeline and load
pipeline = dlt.pipeline(
    pipeline_name='taxi_pipeline',
    destination='duckdb',
    dataset_name='taxi_data',
)

# Run the pipeline
try:
    load_info = pipeline.run(source)
    print(f"Load completed successfully!")
    print(f"Load info: {load_info}")
    
    # Verify the data
    import duckdb
    conn = duckdb.connect('taxi_pipeline.duckdb')
    
    # Check tables
    tables = conn.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'main'").fetchall()
    print(f"\nTables in database: {tables}")
    
    if tables:
        result = conn.execute('SELECT COUNT(*) as record_count FROM taxi_data').fetchone()
        print(f"Total records: {result[0]}")
        result = conn.execute('SELECT MIN(Trip_Pickup_DateTime) as start, MAX(Trip_Pickup_DateTime) as end FROM taxi_data').fetchone()
        print(f"Date range: {result[0]} to {result[1]}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
