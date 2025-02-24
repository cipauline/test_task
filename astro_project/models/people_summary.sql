{{ config(materialized='table') }}

SELECT
    count(DISTINCT name) as people_count
FROM people