CREATE TABLE mining_unit_telemetry (
    unit_id VARCHAR(50) NOT NULL,
    timestamp DATETIME NOT NULL,
    engine_temperature DECIMAL(5,1),
    vibration_level DECIMAL(5,2),
    fuel_level DECIMAL(5,1),
    oil_pressure DECIMAL(5,1),
    brake_temperature DECIMAL(5,1),
    rpm INT,
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    PRIMARY KEY (unit_id, timestamp)
);