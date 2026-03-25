import pyautogui
import time
from zk import ZK
import socket

def cod(resulst):
 
    pyautogui.typewrite(resulst)



# Define the IP and port of the device
device_ip = '172.172.173.135'
device_port = 4370
system_name = socket.gethostname()
system_ip = socket.gethostbyname(system_name)


# Initialize the ZK SDK
zk = ZK(device_ip, port=device_port, timeout=5, password=0, force_udp=False, ommit_ping=False)

def handle_event(conn):
    try:
        # Read the attendance logs
        attendance = conn.get_attendance()
        for att in attendance:
            print(f"User ID: {att.user_id}")
            result = att.user_id
            cod(result)
    except Exception as e:
        print(f"Error reading attendance: {e}")

def monitor_device(conn):
    print("Monitoring for fingerprint events...")
    
    previous_count = len(conn.get_attendance())
    
    while True:
        try:
            current_attendance = conn.get_attendance()
            current_count = len(current_attendance)
            
            if current_count > previous_count:
                new_records = current_attendance[previous_count:]
                for att in new_records:
                    print(f"User ID: {att.user_id}")
                    result = att.user_id
                    cod(result)
                    
                previous_count = current_count

            time.sleep(1)
        except Exception as e:
            print(f"Error during monitoring: {e}")
            break

        
while True:
    print("working")
    try:
        # Connect to the device
        conn = zk.connect()
        print("Connected to the device")

        # Get the device serial number
        # serial_number = conn.get_serialnumber()
        # if serial_number == 'A8N5201060748' and system_ip == '172.172.172.160':
        #     pass
    
        # else:
        #     print("Contact with your Software Developer")
        #     break
        print(f"Device Serial Number:")

        # Disable the device to configure it
        conn.disable_device()
        
        # Monitor device for events
        monitor_device(conn)

    except Exception as e:
        print(f"Error: {e}. Waiting for reconnection...")
        time.sleep(5)  # Wait for 5 seconds before attempting to reconnect

    finally:
        # Disconnect from the device if connected
        if 'conn' in locals() and conn:
            try:
                conn.enable_device()
                conn.disconnect()
                print("Disconnected from the device")
            except Exception as e:
                print(f"Error during disconnection: {e}")
