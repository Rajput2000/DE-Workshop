
-- ANSWER 3
SELECT COUNT(*) from green_taxi_trips
WHERE lpep_pickup_datetime >= '2025-11-01'
AND lpep_pickup_datetime < '2025-12-01'
AND trip_distance <= 1.0;

-- ANSWER 4
SELECT lpep_pickup_datetime::DATE AS pickup_day, trip_distance FROM green_taxi_trips
WHERE trip_distance < 100
ORDER BY trip_distance DESC
LIMIT 5;

-- ANSWER 5
SELECT tz."Zone", SUM(gt.total_amount) AS amount FROM green_taxi_trips AS gt
LEFT JOIN taxi_zones AS tz
ON gt."PULocationID" = tz."LocationID"
WHERE gt.lpep_pickup_datetime >= '2025-11-18 00:00:00' 
  AND gt.lpep_pickup_datetime <  '2025-11-19 00:00:00'
GROUP BY tz."Zone"
ORDER BY amount DESC
LIMIT 10;

-- ANSWER 6
SELECT tz."Zone", gt.tip_amount FROM green_taxi_trips AS gt
LEFT JOIN taxi_zones AS tz
ON gt."DOLocationID" = tz."LocationID"
WHERE gt."PULocationID" =
(SELECT "LocationID" FROM taxi_zones
WHERE "Zone" LIKE 'East Harlem North')
AND lpep_pickup_datetime >= '2025-11-01' 
  AND lpep_pickup_datetime <  '2025-12-01'
ORDER BY gt.tip_amount DESC
LIMIT 5;