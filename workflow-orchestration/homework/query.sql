-- Answer to question 3
SELECT COUNT(*) FROM yellow_tripdata
WHERE filename LIKE '%2020%';

-- Answer to question 4
SELECT COUNT(*) FROM green_tripdata
WHERE filename LIKE '%2020%';

-- Answer to question 5
SELECT COUNT(*) FROM yellow_tripdata
WHERE filename LIKE '%2021%';