from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import EnvironmentSettings, StreamTableEnvironment


def create_green_trips_source(t_env):
    table_name = "green_trips_source"
    t_env.execute_sql(f"""
        CREATE TABLE {table_name} (
            PULocationID INTEGER,
            DOLocationID INTEGER,
            passenger_count DOUBLE,
            trip_distance DOUBLE,
            tip_amount DOUBLE,
            total_amount DOUBLE,
            lpep_pickup_datetime VARCHAR,
            lpep_dropoff_datetime VARCHAR
        ) WITH (
            'connector' = 'kafka',
            'properties.bootstrap.servers' = 'redpanda:29092',
            'topic' = 'green-trips',
            'scan.startup.mode' = 'earliest-offset',
            'properties.auto.offset.reset' = 'earliest',
            'format' = 'json'
        );
    """)
    return table_name


def create_green_trips_sink(t_env):
    table_name = "green_trips_raw"
    t_env.execute_sql(f"""
        CREATE TABLE {table_name} (
            PULocationID INTEGER,
            DOLocationID INTEGER,
            passenger_count DOUBLE,
            trip_distance DOUBLE,
            tip_amount DOUBLE,
            total_amount DOUBLE,
            lpep_pickup_datetime VARCHAR,
            lpep_dropoff_datetime VARCHAR
        ) WITH (
            'connector' = 'jdbc',
            'url' = 'jdbc:postgresql://postgres:5432/postgres',
            'table-name' = '{table_name}',
            'username' = 'postgres',
            'password' = 'postgres',
            'driver' = 'org.postgresql.Driver'
        );
    """)
    return table_name


def run():
    env = StreamExecutionEnvironment.get_execution_environment()
    env.enable_checkpointing(10 * 1000)
    env.set_parallelism(1)

    t_env = StreamTableEnvironment.create(
        env, environment_settings=EnvironmentSettings.new_instance().in_streaming_mode().build()
    )

    try:
        source = create_green_trips_source(t_env)
        sink = create_green_trips_sink(t_env)

        t_env.execute_sql(f"""
            INSERT INTO {sink}
            SELECT
                PULocationID,
                DOLocationID,
                passenger_count,
                trip_distance,
                tip_amount,
                total_amount,
                lpep_pickup_datetime,
                lpep_dropoff_datetime
            FROM {source};
        """).wait()

    except Exception as e:
        print("Flink pass-through job failed:", str(e))


if __name__ == '__main__':
    run()
