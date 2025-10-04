{{
    config(
        materialized='table'
    )
}}

SELECT 
    city, 
    DATE(weather_time_local) AS date,
    ROUND(AVG(temperature)::NUMERIC, 2) AS avg_temperature,
    ROUND(AVG(wind_speed)::NUMERIC, 2) AS avg_wind_speed
FROM {{ ref('stg_weather_data') }}
GROUP BY 
    city, 
    DATE(weather_time_local)
ORDER BY 
    city, 
    DATE(weather_time_local )