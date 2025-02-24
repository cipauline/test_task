CREATE DATABASE astro;

CREATE TABLE astro.raw_data
(
    data String,
    _inserted_at DateTime
)
ENGINE = ReplacingMergeTree(_inserted_at)
ORDER BY tuple();

CREATE TABLE  astro.people 
(
    craft String,
    name String,
    _inserted_at DateTime
) 
ENGINE = ReplacingMergeTree()
ORDER BY (craft, name);

CREATE MATERIALIZED VIEW parsed_raw_data
TO astro.people
AS
SELECT
    JSONExtractString(person, 'craft') as craft,
    JSONExtractString(person, 'name') as name,
    _inserted_at
FROM astro.raw_data
ARRAY JOIN JSONExtractArrayRaw(data, 'people') as person;