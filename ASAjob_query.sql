-- 1. Output raw telemetry as is
SELECT
    unit_id,
    timestamp,
    engine_temperature,
    vibration_level,
    fuel_level,
    oil_pressure,
    brake_temperature,
    rpm,
    latitude,
    longitude
INTO
    [transport-stream-1]
FROM
    [mining-telemetry-streaming]

-- 2. Generate alerts based on thresholds and send to alert output
WITH Alerts AS (
    SELECT
        unit_id,
        timestamp,
        'engine_temperature' AS parameter,
        CAST(engine_temperature AS float) AS value,
        'High Temperature' AS alert_type,
        'High' AS severity,
        'Engine temperature exceeds threshold' AS description
    FROM
        [mining-telemetry-streaming]
    WHERE
        engine_temperature > 90

    UNION ALL

    SELECT
        unit_id,
        timestamp,
        'vibration_level' AS parameter,
        CAST(vibration_level AS float) AS value,
        'High Vibration' AS alert_type,
        'Medium' AS severity,
        'Vibration level exceeds threshold' AS description
    FROM
        [mining-telemetry-streaming]
    WHERE
        vibration_level > 8.0

    UNION ALL

    SELECT
        unit_id,
        timestamp,
        'fuel_level' AS parameter,
        CAST(fuel_level AS float) AS value,
        'Low Fuel' AS alert_type,
        'High' AS severity,
        'Fuel level below threshold' AS description
    FROM
        [mining-telemetry-streaming]
    WHERE
        fuel_level < 22

    UNION ALL

    SELECT
        unit_id,
        timestamp,
        'oil_pressure' AS parameter,
        CAST(oil_pressure AS float) AS value,
        'Low Oil Pressure' AS alert_type,
        'Medium' AS severity,
        'Oil pressure below threshold' AS description
    FROM
        [mining-telemetry-streaming]
    WHERE
        oil_pressure < 35

    UNION ALL

    SELECT
        unit_id,
        timestamp,
        'brake_temperature' AS parameter,
        CAST(brake_temperature AS float) AS value,
        'High Brake Temperature' AS alert_type,
        'High' AS severity,
        'Brake temperature exceeds threshold' AS description
    FROM
        [mining-telemetry-streaming]
    WHERE
        brake_temperature > 260
)

SELECT
    unit_id,
    timestamp,
    parameter,
    value,
    alert_type,
    severity,
    description
INTO
    [mining-alert-log]
FROM Alerts;