from zk import ZK

# --- CONFIGURATION ---
DEVICE_IP = '172.172.173.235'  # Change to your machine IP
DEVICE_PORT = 4370
USER_TO_DELETE = '1182'         # The ID you want to remove

zk = ZK(DEVICE_IP, port=DEVICE_PORT, timeout=5)
conn = None

try:
    print(f"Connecting to device at {DEVICE_IP}...")
    conn = zk.connect()
    
    # Disable the device while making changes (best practice)
    conn.disable_device()
    print(f"✅ Connected. Attempting to delete User ID: {USER_TO_DELETE}")

    # 1. DELETE THE USER
    # Note: user_id is the alphanumeric string (e.g. '1501')
    conn.delete_user(user_id=USER_TO_DELETE)

    print(f"✅ Success! User {USER_TO_DELETE} has been removed from the machine.")

    # Re-enable the device
    conn.enable_device()

except Exception as e:
    print(f"❌ Error: {e}")

finally:
    if conn:
        conn.disconnect()
        print("Disconnected from device.")