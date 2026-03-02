"""Pipeline to ingest NYC taxi data from REST API using dlt."""

import dlt
from dlt.sources.rest_api import rest_api_source


@dlt.source
def taxi_pipeline():
    """NYC taxi data source from REST API with pagination."""
    config = {
        "client": {
            "base_url": "https://us-central1-dlthub-analytics.cloudfunctions.net",
        },
        "resources": [
            {
                "name": "taxi_data",
                "table_name": "taxi_data",
                "endpoint": {
                    "path": "/data_engineering_zoomcamp_api",
                    "paginator": {
                        "type": "page_number",
                        "page_param": "page",
                        "base_page": 1,
                        # Stop pagination when an empty page is returned
                        "stop_after_empty_page": True,
                    },
                    "params": {
                        # Request 1,000 records per page
                        "limit": 1000,
                    },
                },
            },
        ],
    }

    return rest_api_source(config)


if __name__ == "__main__":
    pipeline = dlt.pipeline(
        pipeline_name='taxi_pipeline',
        destination='duckdb',
        dataset_name='taxi_data',
        # show basic progress of resources extracted, normalized files and load-jobs on stdout
        progress="log",
    )

    # Load the data
    load_info = pipeline.run(taxi_pipeline())
    print("Load Info:")
    print(load_info)
    
    # Verify the data
    import duckdb
    conn = duckdb.connect('taxi_pipeline.duckdb')
    result = conn.execute('SELECT COUNT(*) as record_count FROM taxi_data').fetchone()
    print(f"\nTotal records loaded: {result[0]}")
    result = conn.execute('SELECT MIN(CAST(Trip_Pickup_DateTime AS TIMESTAMP)) as start_date, MAX(CAST(Trip_Pickup_DateTime AS TIMESTAMP)) as end_date FROM taxi_data').fetchone()
    print(f"Start date: {result[0]}")
    print(f"End date: {result[1]}")


if __name__ == "__main__":
    load_info = pipeline.run(taxi_pipeline())
    print(load_info)  # noqa: T201
