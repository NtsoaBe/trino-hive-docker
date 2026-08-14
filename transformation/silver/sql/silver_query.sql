MERGE INTO iceberg.project_weather.weather_hourly_silver AS t
USING (
    SELECT
        CAST(from_iso8601_timestamp(raw_time) AS TIMESTAMP(6)) AS time,
        CAST(temperature_2m AS DOUBLE) AS temperature_2m,
        CAST(relative_humidity_2m AS INTEGER) AS relative_humidity_2m,
        CAST(wind_speed_10m AS DOUBLE) AS wind_speed_10m
    FROM iceberg.project_weather.weather_hourly_bronze
) AS s
ON t.time = s.time

WHEN MATCHED THEN
    UPDATE SET
        temperature_2m = s.temperature_2m,
        relative_humidity_2m = s.relative_humidity_2m,
        wind_speed_10m = s.wind_speed_10m

WHEN NOT MATCHED THEN
    INSERT (
        time,
        temperature_2m,
        relative_humidity_2m,
        wind_speed_10m
    )
    VALUES (
        s.time,
        s.temperature_2m,
        s.relative_humidity_2m,
        s.wind_speed_10m
    )
