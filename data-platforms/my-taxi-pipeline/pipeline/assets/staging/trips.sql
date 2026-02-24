/* @bruin

# Docs:
# - Materialization: https://getbruin.com/docs/bruin/assets/materialization
# - Quality checks (built-ins): https://getbruin.com/docs/bruin/quality/available_checks
# - Custom checks: https://getbruin.com/docs/bruin/quality/custom

# TODO: Set the asset name (recommended: staging.trips).
name: staging.trips
# TODO: Set platform type.
# Docs: https://getbruin.com/docs/bruin/assets/sql
# suggested type: duckdb.sql
type: duckdb.sql

# TODO: Declare dependencies so `bruin run ... --downstream` and lineage work.
# Examples:
# depends:
#   - ingestion.trips
#   - ingestion.payment_lookup
depends:
  - ingestion.trips
  - ingestion.payment_lookup

# TODO: Choose time-based incremental processing if the dataset is naturally time-windowed.
# - This module expects you to use `time_interval` to reprocess only the requested window.
materialization:
  # What is materialization?
  # Materialization tells Bruin how to turn your SELECT query into a persisted dataset.
  # Docs: https://getbruin.com/docs/bruin/assets/materialization
  #
  # Materialization "type":
  # - table: persisted table
  # - view: persisted view (if the platform supports it)
  type: table
  strategy: create+replace

# TODO: Define output columns, mark primary keys, and add a few checks.
columns:
  - name: pickup_datetime
    type: timestamp
    description: The timestamp when the trip started
    primary_key: true
    nullable: false
    checks:
      - name: not_null


# TODO: Add one custom check that validates a staging invariant (uniqueness, ranges, etc.)
# Docs: https://getbruin.com/docs/bruin/quality/custom
custom_checks:
  - name: row_count_greater_than_zero
    description: Ensure that the staging table has at least one row
    query: |
      -- TODO: return a single scalar (COUNT(*), etc.) that should match `value`
      SELECT CASE WHEN COUNT(*) > 0 THEN 1 ELSE 0 END
      FROM staging.trips
    value: 1

@bruin */

-- TODO: Write the staging SELECT query.
--
-- Purpose of staging:
-- - Clean and normalize schema from ingestion
-- - Deduplicate records (important if ingestion uses append strategy)
-- - Enrich with lookup tables (JOINs)
-- - Filter invalid rows (null PKs, negative values, etc.)
--
-- Why filter by {{ start_datetime }} / {{ end_datetime }}?
-- When using `time_interval` strategy, Bruin:
--   1. DELETES rows where `incremental_key` falls within the run's time window
--   2. INSERTS the result of your query
-- Therefore, your query MUST filter to the same time window so only that subset is inserted.
-- If you don't filter, you'll insert ALL data but only delete the window's data = duplicates.

SELECT
    t.tpep_pickup_datetime AS pickup_datetime,
    t.tpep_dropoff_datetime AS dropoff_datetime,
    t.pu_location_id AS pickup_location_id,
    t.do_location_id AS dropoff_location_id,
    t.fare_amount,
    t.taxi_type,
    p.payment_type_name
FROM ingestion.trips t
LEFT JOIN ingestion.payment_lookup p
    ON t.payment_type = p.payment_type_id
WHERE t.tpep_pickup_datetime >= '{{ start_datetime }}'
  AND t.tpep_pickup_datetime < '{{ end_datetime }}'
QUALIFY ROW_NUMBER() OVER (
    PARTITION BY t.tpep_pickup_datetime, t.tpep_dropoff_datetime,
                 t.pu_location_id, t.do_location_id, t.fare_amount
    ORDER BY t.tpep_pickup_datetime
) = 1