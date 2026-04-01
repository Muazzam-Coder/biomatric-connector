import time
import requests
from zk import ZK

# --- CONFIGURATION ---
DEVICE_IP = '172.172.173.234'
DEVICE_PORT = 4370
FLOOR_ID = 3 

# SERVER DETAILS
# Replace the path below with the actual URL pointing to CameraCheckInView
SERVER_IP = '172.172.173.102'
SERVER_PORT = '1234'
SERVER_URL = f"http://{SERVER_IP}:{SERVER_PORT}/cin/" 

def monitor_device():
    zk = ZK(DEVICE_IP, port=DEVICE_PORT, timeout=1)
    conn = None
    try:
        conn = zk.connect()
        print(f"✅ Connected to Biometric Device: {DEVICE_IP}")
        
        # Get initial count to ignore old history
        attendance = conn.get_attendance()
        last_count = len(attendance)
        print(f"Monitoring started. Initial log count: {last_count}")

        while True:
            attendance = conn.get_attendance()
            current_count = len(attendance)

            if current_count > last_count:
                # Process only the new thumb scans
                new_records = attendance[last_count:]
                for log in new_records:
                    print(f"New Thumb Scan: User {log.user_id}")
                    
                    # PREPARE DATA FOR CameraCheckInView
                    payload = {
                        "employee_id": log.user_id,
                        "floor": FLOOR_ID
                    }
                    
                    # SEND POST REQUEST
                    try:
                        response = requests.post(SERVER_URL, json=payload, timeout=0.1)
                        if response.status_code == 201:
                            data = response.json()
                            print(f"✅ Success: {data['emp_name']} checked in.")
                        else:
                            print(f"❌ Server Error ({response.status_code}): {response.text}")
                    except Exception as e:
                        print(f"❌ Network Error: {e}")

                # Update the count
                last_count = current_count
            
            # time.sleep(1) # Wait 1 second before checking again

    except Exception as e:
        print(f"⚠️ Device Error: {e}")
    

if __name__ == "__main__":
    while True:
        monitor_device()
        print("Retrying connection in 1 seconds...")
        time.sleep(1)