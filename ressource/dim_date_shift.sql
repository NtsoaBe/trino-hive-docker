WITH hourly_calendar AS (
    SELECT ts
    FROM UNNEST(
        SEQUENCE(
            TIMESTAMP '2026-01-01 00:00:00',
            TIMESTAMP '2026-09-30 23:00:00',
            INTERVAL '1' HOUR
        )
    ) AS t(ts)
)

SELECT
    CAST(ts AS DATE) AS dt,
    CAST(ts AS TIME) AS ts,
    hour(ts) AS hour_of_day,
    CASE
        WHEN hour(ts) >= 6
         AND hour(ts) < 18 THEN 'Day'
        ELSE 'Night'
    END AS shift
FROM hourly_calendar
ORDER BY dt, ts;