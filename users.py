import pandas as pd
from zk import ZK

# --- CONFIGURATION ---
DEVICE_IP = '172.172.173.232'  # This will also be the filename
DEVICE_PORT = 4370

zk = ZK(DEVICE_IP, port=DEVICE_PORT, timeout=5)
conn = None

try:
    print(f"Connecting to device at {DEVICE_IP}...")
    conn = zk.connect()
    print("✅ Connected! Fetching user list...")

    # Fetch all users
    users = conn.get_users()
    
    # Create a list of dictionaries for the Excel rows
    user_data = []
    for user in users:
        user_data.append({
            "Internal_UID": user.uid,
            "Employee_ID": user.user_id,
            "Name": user.name,
            "Privilege": "Admin" if user.privilege == 14 else "User",
            "Password": user.password if user.password else ""
        })

    # Create a Pandas DataFrame
    df = pd.DataFrame(user_data)

    # Define filename based on IP
    # We replace dots with underscores if you prefer, but dots work fine for filenames
    file_name = f"{DEVICE_IP}.xlsx"

    # Export to Excel
    df.to_excel(file_name, index=False)

    print("-" * 40)
    print(f"✅ SUCCESS!")
    print(f"Total Employees Exported: {len(users)}")
    print(f"File Saved As: {file_name}")
    print("-" * 40)

except Exception as e:
    print(f"❌ Error: {e}")

finally:
    if conn:
        conn.disconnect()
        print("Disconnected from device.")