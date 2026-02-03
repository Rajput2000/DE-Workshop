-- Answer to question 1
SELECT COUNT(*) FROM `organic-phoenix-484620-p3.zoomcamp.yellow_tripdata`;

-- Answer to question 2: Count distinct PULocationIDs
-- External Table
SELECT COUNT(DISTINCT PULocationID) 
FROM `organic-phoenix-484620-p3.zoomcamp.yellow_tripdata_external`;

-- Regular Table
SELECT COUNT(DISTINCT PULocationID) 
FROM `organic-phoenix-484620-p3.zoomcamp.yellow_tripdata`;

-- Answer to question 4
SELECT COUNT(*) FROM `organic-phoenix-484620-p3.zoomcamp.yellow_tripdata`
WHERE fare_amount = 0;

-- Answer to question 5
CREATE OR REPLACE TABLE `organic-phoenix-484620-p3.zoomcamp.yellow_tripdata_partitioned_clustered`
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID
AS
SELECT * FROM `organic-phoenix-484620-p3.zoomcamp.yellow_tripdata`;

-- Answer to question 6
SELECT DISTINCT VendorID
FROM `organic-phoenix-484620-p3.zoomcamp.yellow_tripdata_partitioned_clustered`
WHERE DATE(tpep_dropoff_datetime) BETWEEN '2024-03-01' AND '2024-03-15';

