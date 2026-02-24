import pandas as pd

# Read parquet file
df = pd.read_parquet('analytics-engineering/yellow_tripdata_2024-01.parquet')

# Display the table
print(df)

# Display datatypes
print("\nData Types:")
print(df.dtypes)
print("\nDataFrame Info:")
print(df.info())
print("\nDataFrame")
print(df)