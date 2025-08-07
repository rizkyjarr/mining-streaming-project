import time
import json
import random
import threading
import signal
from azure.iot.device import IoTHubDeviceClient, Message
from dotenv import load_dotenv
import os
from datetime import datetime
import pytz

# Load environment variables
load_dotenv()

# Device connection strings from .env
DEVICE_CONNECTION_STRINGS = {
    "HD785-7-001": os.getenv("DEVICE_HD785_7_001"),
    "HD785-7-002": os.getenv("DEVICE_HD785_7_002"),
    "HD785-7-003": os.getenv("DEVICE_HD785_7_003")
}

# Shutdown flag for Ctrl+C
shutdown_event = threading.Event()

# Get Jakarta time
def get_jakarta_timestamp():
    jakarta_tz = pytz.timezone('Asia/Jakarta')
    now = datetime.now(jakarta_tz)
    return now.strftime('%Y-%m-%d %H:%M:%S')

# Generate telemetry as you wanted
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
        "latitude": -1.23456 + random.uniform(-0.01, 0.01),
        "longitude": 117.12345 + random.uniform(-0.01, 0.01)        
    }
    return data

# Simulate telemetry sending per unit
def simulate_unit(unit_name, conn_str):
    try:
        client = IoTHubDeviceClient.create_from_connection_string(conn_str)
        client.connect()
        print(f"[{unit_name}] Connected")

        while not shutdown_event.is_set():
            data = generate_fake_telemetry(unit_name)
            message = Message(json.dumps(data))
            client.send_message(message)
            print(f"[{unit_name}] Sent: {data}")
            time.sleep(60)

    except Exception as e:
        print(f"[{unit_name}] Error: {e}")
    finally:
        try:
            client.shutdown()
            print(f"[{unit_name}] Disconnected")
        except:
            pass

# Ctrl+C handling
def handle_sigint(signum, frame):
    print("\n🛑 Ctrl+C received! Stopping all units...")
    shutdown_event.set()

signal.signal(signal.SIGINT, handle_sigint)

# Launch simulation threads
threads = []
for unit, conn_str in DEVICE_CONNECTION_STRINGS.items():
    if conn_str:
        t = threading.Thread(target=simulate_unit, args=(unit, conn_str))
        t.start()
        threads.append(t)
    else:
        print(f"[{unit}] Skipped: Connection string not set in .env")

# Wait for all threads to finish
for t in threads:
    t.join()

print("✅ All units stopped.")