"""NYC Taxi data pipeline using dlt REST API source."""

import dlt
from dlt.sources.rest_api import rest_api_resources
from dlt.sources.rest_api.typing import RESTAPIConfig


@dlt.source
def taxi_rest_api_source():
    """Define dlt resources from NYC Taxi REST API endpoints."""
    config: RESTAPIConfig = {
        "client": {
            "base_url": "https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api",
        },
        "resource_defaults": {
            "write_disposition": "replace",
        },
        "resources": [
            {
                "name": "taxi_trips",
                "endpoint": {
                    "path": "",
                    "method": "GET",
                    "params": {
                        "limit": 1000,
                        "offset": 0
                    },
                    "data_selector": "$",
                    "paginator": {
                        "type": "offset",
                        "limit": 1000,
                        "offset": 0,
                        "offset_param": "offset",
                        "limit_param": "limit",
                        "stop_after_empty_page": True
                    }
                }
            }
        ],
    }

    yield from rest_api_resources(config)


pipeline = dlt.pipeline(
    pipeline_name='taxi_pipeline',
    destination='duckdb',
    refresh="drop_sources",
    progress="log",
)


if __name__ == "__main__":
    load_info = pipeline.run(taxi_rest_api_source())
    print(load_info)