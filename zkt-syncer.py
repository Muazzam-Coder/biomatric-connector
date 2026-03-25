import customtkinter as ctk
from zk import ZK
import threading
import time
import os

# Set UI Theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ZKSyncApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ZK Biometric Multi-Device Syncer")
        self.geometry("700x600")

        # --- ADD LOGO TO TITLE BAR ---
        try:
            # Path to your icon file
            icon_path = "zkt-syncer-logo.ico"
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
        except Exception as e:
            print(f"Could not load icon: {e}")

        # --- UI LAYOUT ---
        # Header
        self.header = ctk.CTkLabel(self, text="Biometric Data Synchronization", font=("Roboto", 24, "bold"))
        self.header.pack(pady=20)

        # Source IP Input
        self.src_label = ctk.CTkLabel(self, text="Source Machine IP:")
        self.src_label.pack(padx=20, anchor="w")
        self.src_entry = ctk.CTkEntry(self, width=660, placeholder_text="e.g. 172.172.173.235")
        self.src_entry.insert(0, "172.172.173.235")
        self.src_entry.pack(padx=20, pady=(0, 15))

        # Target IP Input
        self.tgt_label = ctk.CTkLabel(self, text="Target Machine IPs (Comma Separated):")
        self.tgt_label.pack(padx=20, anchor="w")
        self.tgt_entry = ctk.CTkTextbox(self, width=660, height=80)
        self.tgt_entry.insert("0.0", "172.172.173.234, 172.172.173.232")
        self.tgt_entry.pack(padx=20, pady=(0, 15))

        # Progress Log
        self.log_label = ctk.CTkLabel(self, text="Process Log:")
        self.log_label.pack(padx=20, anchor="w")
        self.log_box = ctk.CTkTextbox(self, width=660, height=200, state="disabled", font=("Consolas", 12))
        self.log_box.pack(padx=20, pady=(0, 15))

        # Control Buttons
        self.sync_button = ctk.CTkButton(self, text="Start Synchronization", command=self.start_sync_thread, height=45, font=("Roboto", 16, "bold"))
        self.sync_button.pack(padx=20, pady=10, fill="x")

        self.status_bar = ctk.CTkLabel(self, text="Ready", text_color="gray")
        self.status_bar.pack(pady=5)

    def log(self, message):
        """Thread-safe logging to the UI"""
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"[{time.strftime('%H:%M:%S')}] {message}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def start_sync_thread(self):
        """Runs the sync logic in a background thread to keep UI responsive"""
        self.sync_button.configure(state="disabled", text="Syncing... Please wait")
        self.status_bar.configure(text_color="yellow", text="Processing...")
        
        # Get data from UI
        source_ip = self.src_entry.get().strip()
        targets_raw = self.tgt_entry.get("0.0", "end").strip()
        target_ips = [ip.strip() for ip in targets_raw.split(",") if ip.strip()]

        thread = threading.Thread(target=self.run_sync, args=(source_ip, target_ips), daemon=True)
        thread.start()

    def run_sync(self, source_ip, target_ips):
        try:
            self.log(f"--- STARTING NEW SESSION ---")
            self.log(f"Connecting to Source: {source_ip}...")
            zk_src = ZK(source_ip, port=4370, timeout=5)
            conn_src = zk_src.connect()
            
            self.log("Fetching Source Database...")
            users = conn_src.get_users()
            templates = conn_src.get_templates()
            self.log(f"Found {len(users)} users and {len(templates)} fingerprints.")
            
            # Loop through each target IP
            for target_ip in target_ips:
                self.log(f"\n>>> Connecting to Target: {target_ip}...")
                try:
                    zk_tgt = ZK(target_ip, port=4370, timeout=5)
                    conn_tgt = zk_tgt.connect()
                    
                    u_success = 0
                    f_success = 0

                    for user in users:
                        try:
                            # 1. Sync User
                            conn_tgt.set_user(
                                uid=user.uid,
                                name=user.name,
                                privilege=user.privilege,
                                user_id=user.user_id
                            )
                            u_success += 1
                            
                            # 2. Sync Fingers for this user
                            user_fingers = [t for t in templates if t.uid == user.uid]
                            for f in user_fingers:
                                try:
                                    # Passing (user, template) as per library requirements
                                    conn_tgt.save_user_template(user, f)
                                    f_success += 1
                                except:
                                    continue
                            
                            self.status_bar.configure(text=f"Syncing {target_ip}: User {user.user_id}")
                        except Exception as e:
                            self.log(f"Error syncing user {user.user_id}: {e}")

                    self.log(f"✅ Success for {target_ip}: {u_success} Users, {f_success} Fingers.")
                    conn_tgt.disconnect()
                
                except Exception as e:
                    self.log(f"❌ Could not connect to {target_ip}: {e}")

            conn_src.disconnect()
            self.log("\n--- ALL TASKS COMPLETED ---")
            self.status_bar.configure(text_color="green", text="All Done!")

        except Exception as e:
            self.log(f"❌ CRITICAL ERROR: {e}")
            self.status_bar.configure(text_color="red", text="Process Failed")

        finally:
            self.sync_button.configure(state="normal", text="Start Synchronization")

if __name__ == "__main__":
    app = ZKSyncApp()
    app.mainloop()