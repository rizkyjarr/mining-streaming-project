import time
import json
import random
import threading
import signal
from azure.iot.device import IoTHubDeviceClient, Message
from dotenv import load_dotenv
import os

# Load env
load_dotenv()

# Replace with your actual device connection strings
DEVICE_CONNECTION_STRINGS = {
    "HD785-7-001": os.getenv("DEVICE_HD785_7_001"),
    "HD785-7-002": os.getenv("DEVICE_HD785_7_002"),
    "HD785-7-003": os.getenv("DEVICE_HD785_7_003")
}

# Shared shutdown flag
shutdown_event = threading.Event()

def simulate_unit(unit_name, conn_str):
    try:
        client = IoTHubDeviceClient.create_from_connection_string(conn_str)
        client.connect()
        print(f"[{unit_name}] Connected")

        while not shutdown_event.is_set():
            data = {
                "unit_id": unit_name,
                "temperature": round(random.uniform(25, 35), 2),
                "humidity": round(random.uniform(30, 60), 2),
                "vibration": round(random.uniform(0.1, 1.0), 3),
                "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
            }
            message = Message(json.dumps(data))
            client.send_message(message)
            print(f"[{unit_name}] Sent: {data}")
            time.sleep(20)

    except Exception as e:
        print(f"[{unit_name}] Error: {e}")
    finally:
        try:
            client.shutdown()
            print(f"[{unit_name}] Disconnected")
        except:
            pass

# Handle Ctrl+C to trigger shutdown_event
def handle_sigint(signum, frame):
    print("\n🛑 Ctrl+C received! Stopping all units...")
    shutdown_event.set()

# Bind signal
signal.signal(signal.SIGINT, handle_sigint)

# Start each unit's simulation in a thread
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
