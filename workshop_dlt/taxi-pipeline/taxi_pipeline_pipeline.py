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


pipeline = dlt.pipeline(
    pipeline_name='taxi_pipeline',
    destination='duckdb',
    dataset_name='taxi_data',
    # `refresh="drop_sources"` ensures the data and the state is cleaned
    # on each `pipeline.run()`; remove the argument once you have a
    # working pipeline.
    refresh="drop_sources",
    # show basic progress of resources extracted, normalized files and load-jobs on stdout
    progress="log",
)


if __name__ == "__main__":
    load_info = pipeline.run(taxi_pipeline())
    print(load_info)  # noqa: T201
