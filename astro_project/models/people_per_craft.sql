{{ config(materialized='table') }}

SELECT
    craft, count(DISTINCT name) as people_count
FROM people
GROUP BY craft