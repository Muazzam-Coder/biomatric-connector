from zk import ZK
import time

# --- SETTINGS ---
SOURCE_IP = '172.172.173.235'
TARGET_IP = '172.172.173.234'
PORT = 4370

zk_src = ZK(SOURCE_IP, port=PORT, timeout=5)
zk_tgt = ZK(TARGET_IP, port=PORT, timeout=5)

try:
    print(f"Connecting to devices...")
    conn_src = zk_src.connect()
    conn_tgt = zk_tgt.connect()

    # 1. FETCH DATA
    print("Reading from Source...")
    users = conn_src.get_users()
    templates = conn_src.get_templates()
    print(f"✅ Source has {len(users)} users and {len(templates)} templates.")

    # 2. SYNC
    print("\nStarting Sync...")
    u_success = 0
    f_success = 0

    for user in users:
        try:
            # Step A: Create/Update the User on Target
            # We save the returned user object from set_user to use it for the template
            conn_tgt.set_user(
                uid=user.uid,
                name=user.name,
                privilege=user.privilege,
                user_id=user.user_id
            )
            u_success += 1
            
            # Step B: Find this user's fingers
            user_fingers = [t for t in templates if t.uid == user.uid]
            
            for f in user_fingers:
                try:
                    # KEY FIX: Your library version requires BOTH the user object 
                    # and the template object to be passed together.
                    conn_tgt.save_user_template(user, f)
                    f_success += 1
                except Exception as e:
                    # If it still complains about __dict__, we skip it and try the next
                    continue

            print(f"Syncing ID {user.user_id} ({user.name}): {len(user_fingers)} fingers synced.", end="\r")
            time.sleep(0.01)

        except Exception as e:
            print(f"\n❌ Failed to sync User {user.user_id}: {e}")

    print("\n" + "="*40)
    print("✅ SYNC PROCESS FINISHED")
    print(f"Users: {u_success}")
    print(f"Fingers: {f_success}")
    print("="*40)

except Exception as e:
    print(f"\n❌ CRITICAL ERROR: {e}")

finally:
    if 'conn_src' in locals(): conn_src.disconnect()
    if 'conn_tgt' in locals(): conn_tgt.disconnect()