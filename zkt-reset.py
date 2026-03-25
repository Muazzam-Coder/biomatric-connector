from zk import ZK

# --- TARGET MACHINE ---
TARGET_IP = '172.172.173.234'
zk = ZK(TARGET_IP, port=4370, timeout=5)

try:
    print(f"Connecting to {TARGET_IP} to unlock...")
    conn = zk.connect()
    users = conn.get_users()
    
    # We will set EVERY user to privilege 0 (Normal User)
    # This removes any Admin locks so you can open the Menu.
    for user in users:
        if user.privilege > 0: # If they are an Admin
            print(f"Demoting Admin: {user.name} (ID: {user.user_id}) to Normal User...")
            conn.set_user(
                uid=user.uid,
                name=user.name,
                privilege=0, # 0 = Normal User
                password=user.password,
                user_id=user.user_id
            )
            
    print("\n✅ SUCCESS! The machine is now UNLOCKED.")
    print("ACTION: Go to the machine and press 'M/OK'. It should open the menu now.")
    conn.disconnect()
except Exception as e:
    print(f"Error: {e}")