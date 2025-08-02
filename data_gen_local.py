import time
import random
import json
import threading
import pytz
import datetime

def get_jakarta_timestamp():
    jakarta_tz = pytz.timezone('Asia/Jakarta')
    now = datetime.datetime.now(jakarta_tz)
    return now.strftime('%Y-%m-%dT%H:%M:%S%z')  # e.g. '2025-08-02T21:35:10+0700'

def generate_fake_telemetry(unit_id):
    data = {
        "unit_id": unit_id,
        "timestamp": get_jakarta_timestamp(),
        "engine_temperature": round(random.uniform(75, 100), 1),
        "vibration_level": round(random.uniform(2.0, 10.0), 2),
        "fuel_level": round(random.uniform(20, 100), 1),
        "oil_pressure": round(random.uniform(30, 60), 1),
        "brake_temperature": round(random.uniform(180, 280), 1),
        "rpm": random.randint(900, 1800),
        "location": {
            "lat": -1.23456 + random.uniform(-0.01, 0.01),
            "lon": 117.12345 + random.uniform(-0.01, 0.01)
        }
    }
    return data

def simulate_unit(unit_id):
    while True:
        telemetry = generate_fake_telemetry(unit_id)
        print(f"[{unit_id}] {json.dumps(telemetry, indent=2)}\n")
        time.sleep(5)

if __name__ == "__main__":
    unit_ids = ["HD785-7-001", "HD785-7-002", "HD785-7-003"]
    threads = []

    for unit_id in unit_ids:
        t = threading.Thread(target=simulate_unit, args=(unit_id,), daemon=True)
        t.start()
        threads.append(t)

    # Keep main thread alive
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("Stopped by user.")