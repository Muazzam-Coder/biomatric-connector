# import customtkinter as ctk
# from zk import ZK
# import threading
# import time
# import os

# # Set UI Theme
# ctk.set_appearance_mode("Dark")
# ctk.set_default_color_theme("blue")

# class ZKSyncApp(ctk.CTk):
#     def __init__(self):
#         super().__init__()

#         self.title("ZK Biometric Multi-Device Syncer")
#         self.geometry("700x600")

#         # --- ADD LOGO TO TITLE BAR ---
#         try:
#             # Path to your icon file
#             icon_path = "zkt-syncer-logo.ico"
#             if os.path.exists(icon_path):
#                 self.iconbitmap(icon_path)
#         except Exception as e:
#             print(f"Could not load icon: {e}")

#         # --- UI LAYOUT ---
#         # Header
#         self.header = ctk.CTkLabel(self, text="Biometric Data Synchronization", font=("Roboto", 24, "bold"))
#         self.header.pack(pady=20)

#         # Source IP Input
#         self.src_label = ctk.CTkLabel(self, text="Source Machine IP:")
#         self.src_label.pack(padx=20, anchor="w")
#         self.src_entry = ctk.CTkEntry(self, width=660, placeholder_text="e.g. 172.172.173.235")
#         self.src_entry.insert(0, "172.172.173.235")
#         self.src_entry.pack(padx=20, pady=(0, 15))

#         # Target IP Input
#         self.tgt_label = ctk.CTkLabel(self, text="Target Machine IPs (Comma Separated):")
#         self.tgt_label.pack(padx=20, anchor="w")
#         self.tgt_entry = ctk.CTkTextbox(self, width=660, height=80)
#         self.tgt_entry.insert("0.0", "172.172.173.234, 172.172.173.232")
#         self.tgt_entry.pack(padx=20, pady=(0, 15))

#         # Progress Log
#         self.log_label = ctk.CTkLabel(self, text="Process Log:")
#         self.log_label.pack(padx=20, anchor="w")
#         self.log_box = ctk.CTkTextbox(self, width=660, height=200, state="disabled", font=("Consolas", 12))
#         self.log_box.pack(padx=20, pady=(0, 15))

#         # Control Buttons
#         self.sync_button = ctk.CTkButton(self, text="Start Synchronization", command=self.start_sync_thread, height=45, font=("Roboto", 16, "bold"))
#         self.sync_button.pack(padx=20, pady=10, fill="x")

#         self.status_bar = ctk.CTkLabel(self, text="Ready", text_color="gray")
#         self.status_bar.pack(pady=5)

#     def log(self, message):
#         """Thread-safe logging to the UI"""
#         self.log_box.configure(state="normal")
#         self.log_box.insert("end", f"[{time.strftime('%H:%M:%S')}] {message}\n")
#         self.log_box.see("end")
#         self.log_box.configure(state="disabled")

#     def start_sync_thread(self):
#         """Runs the sync logic in a background thread to keep UI responsive"""
#         self.sync_button.configure(state="disabled", text="Syncing... Please wait")
#         self.status_bar.configure(text_color="yellow", text="Processing...")
        
#         # Get data from UI
#         source_ip = self.src_entry.get().strip()
#         targets_raw = self.tgt_entry.get("0.0", "end").strip()
#         target_ips = [ip.strip() for ip in targets_raw.split(",") if ip.strip()]

#         thread = threading.Thread(target=self.run_sync, args=(source_ip, target_ips), daemon=True)
#         thread.start()

#     def run_sync(self, source_ip, target_ips):
#         try:
#             self.log(f"--- STARTING NEW SESSION ---")
#             self.log(f"Connecting to Source: {source_ip}...")
#             zk_src = ZK(source_ip, port=4370, timeout=5)
#             conn_src = zk_src.connect()
            
#             self.log("Fetching Source Database...")
#             users = conn_src.get_users()
#             templates = conn_src.get_templates()
#             self.log(f"Found {len(users)} users and {len(templates)} fingerprints.")
            
#             # Loop through each target IP
#             for target_ip in target_ips:
#                 self.log(f"\n>>> Connecting to Target: {target_ip}...")
#                 try:
#                     zk_tgt = ZK(target_ip, port=4370, timeout=5)
#                     conn_tgt = zk_tgt.connect()
                    
#                     u_success = 0
#                     f_success = 0

#                     for user in users:
#                         try:
#                             # 1. Sync User
#                             conn_tgt.set_user(
#                                 uid=user.uid,
#                                 name=user.name,
#                                 privilege=user.privilege,
#                                 user_id=user.user_id
#                             )
#                             u_success += 1
                            
#                             # 2. Sync Fingers for this user
#                             user_fingers = [t for t in templates if t.uid == user.uid]
#                             for f in user_fingers:
#                                 try:
#                                     # Passing (user, template) as per library requirements
#                                     conn_tgt.save_user_template(user, f)
#                                     f_success += 1
#                                 except:
#                                     continue
                            
#                             self.status_bar.configure(text=f"Syncing {target_ip}: User {user.user_id}")
#                         except Exception as e:
#                             self.log(f"Error syncing user {user.user_id}: {e}")

#                     self.log(f"✅ Success for {target_ip}: {u_success} Users, {f_success} Fingers.")
#                     conn_tgt.disconnect()
                
#                 except Exception as e:
#                     self.log(f"❌ Could not connect to {target_ip}: {e}")

#             conn_src.disconnect()
#             self.log("\n--- ALL TASKS COMPLETED ---")
#             self.status_bar.configure(text_color="green", text="All Done!")

#         except Exception as e:
#             self.log(f"❌ CRITICAL ERROR: {e}")
#             self.status_bar.configure(text_color="red", text="Process Failed")

#         finally:
#             self.sync_button.configure(state="normal", text="Start Synchronization")

# if __name__ == "__main__":
#     app = ZKSyncApp()
#     app.mainloop()
















# import customtkinter as ctk
# from zk import ZK
# import threading
# import time
# import os

# ctk.set_appearance_mode("Dark")
# ctk.set_default_color_theme("blue")

# class ZKSyncApp(ctk.CTk):
#     def __init__(self):
#         super().__init__()
#         self.title("ZK Smart Delta Syncer Pro")
#         self.geometry("700x650")

#         try:
#             if os.path.exists("zkt-syncer-logo.ico"): self.iconbitmap("zkt-syncer-logo.ico")
#         except: pass

#         # --- UI LAYOUT ---
#         self.header = ctk.CTkLabel(self, text="Smart Delta Synchronization", font=("Roboto", 24, "bold"))
#         self.header.pack(pady=20)

#         self.src_entry = ctk.CTkEntry(self, width=660)
#         self.src_entry.insert(0, "172.172.173.235")
#         self.src_entry.pack(padx=20, pady=10)

#         self.tgt_entry = ctk.CTkTextbox(self, width=660, height=80)
#         self.tgt_entry.insert("0.0", "172.172.173.234")
#         self.tgt_entry.pack(padx=20, pady=10)

#         self.mirror_var = ctk.BooleanVar(value=True)
#         self.mirror_switch = ctk.CTkSwitch(self, text="Mirror Mode (Delete users from Target if removed from Source)", variable=self.mirror_var)
#         self.mirror_switch.pack(padx=20, pady=5, anchor="w")

#         self.log_box = ctk.CTkTextbox(self, width=660, height=250, state="disabled", font=("Consolas", 11))
#         self.log_box.pack(padx=20, pady=15)

#         self.sync_button = ctk.CTkButton(self, text="Run Smart Sync", command=self.start_sync_thread, height=45, font=("Roboto", 16, "bold"))
#         self.sync_button.pack(padx=20, pady=10, fill="x")

#         self.status_bar = ctk.CTkLabel(self, text="Ready", text_color="gray")
#         self.status_bar.pack(pady=5)

#     def log(self, message):
#         self.log_box.configure(state="normal")
#         self.log_box.insert("end", f"[{time.strftime('%H:%M:%S')}] {message}\n")
#         self.log_box.see("end")
#         self.log_box.configure(state="disabled")

#     def start_sync_thread(self):
#         self.sync_button.configure(state="disabled", text="Analyzing...")
#         source_ip = self.src_entry.get().strip()
#         targets_raw = self.tgt_entry.get("0.0", "end").strip()
#         target_ips = [ip.strip() for ip in targets_raw.split(",") if ip.strip()]
#         threading.Thread(target=self.run_delta_sync, args=(source_ip, target_ips), daemon=True).start()

#     def run_delta_sync(self, source_ip, target_ips):
#         try:
#             self.log("--- ANALYZING SOURCE MACHINE ---")
#             zk_src = ZK(source_ip, port=4370, timeout=5)
#             conn_src = zk_src.connect()
            
#             src_users = conn_src.get_users()
#             src_templates = conn_src.get_templates()
            
#             # Map source users by ID
#             src_user_map = {u.user_id: u for u in src_users}
#             # Map source templates by UID
#             src_temp_map = {}
#             for t in src_templates:
#                 if t.uid not in src_temp_map: src_temp_map[t.uid] = []
#                 src_temp_map[t.uid].append(t)

#             self.log(f"Source: {len(src_users)} users, {len(src_templates)} fingerprints found.")

#             for target_ip in target_ips:
#                 self.log(f"\n--- SYNCING TARGET: {target_ip} ---")
#                 try:
#                     zk_tgt = ZK(target_ip, port=4370, timeout=5)
#                     conn_tgt = zk_tgt.connect()
#                     conn_tgt.disable_device()

#                     tgt_users = conn_tgt.get_users()
#                     tgt_templates = conn_tgt.get_templates()
                    
#                     tgt_user_map = {u.user_id: u for u in tgt_users}
#                     tgt_temp_count = {} # Count fingers per user on target
#                     for t in tgt_templates:
#                         # Find the user_id associated with this UID on target
#                         # (Necessary because UIDs might differ, but user_ids are unique)
#                         t_user = next((u for u in tgt_users if u.uid == t.uid), None)
#                         if t_user:
#                             tgt_temp_count[t_user.user_id] = tgt_temp_count.get(t_user.user_id, 0) + 1

#                     # 1. DELETE LOGIC (MIRROR)
#                     if self.mirror_var.get():
#                         for t_id in list(tgt_user_map.keys()):
#                             if t_id not in src_user_map:
#                                 self.log(f"  🗑️ Removing User {t_id} (Deleted from Source)")
#                                 conn_tgt.delete_user(user_id=t_id)

#                     # 2. UPDATE / ADD LOGIC
#                     sync_needed = 0
#                     for s_id, s_user in src_user_map.items():
#                         t_user = tgt_user_map.get(s_id)
#                         s_user_templates = src_temp_map.get(s_user.uid, [])
                        
#                         is_new = t_user is None
#                         name_diff = t_user and t_user.name != s_user.name
#                         priv_diff = t_user and t_user.privilege != s_user.privilege
#                         temp_diff = t_user and len(s_user_templates) != tgt_temp_count.get(s_id, 0)

#                         if is_new or name_diff or priv_diff or temp_diff:
#                             action = "Adding" if is_new else "Updating"
#                             self.log(f"  🔄 {action} User {s_id} ({s_user.name})")
                            
#                             # Push User Profile
#                             conn_tgt.set_user(uid=s_user.uid, name=s_user.name, 
#                                             privilege=s_user.privilege, user_id=s_user.user_id)
                            
#                             # Push Templates (If count changed or new)
#                             for f in s_user_templates:
#                                 conn_tgt.save_user_template(s_user, f)
                            
#                             sync_needed += 1

#                     if sync_needed == 0:
#                         self.log("  ✨ Target is already up to date. No sync needed.")
#                     else:
#                         self.log(f"  ✅ Successfully updated {sync_needed} records.")

#                     conn_tgt.enable_device()
#                     conn_tgt.disconnect()
#                 except Exception as e:
#                     self.log(f"  ❌ Error on {target_ip}: {e}")

#             conn_src.disconnect()
#             self.status_bar.configure(text_color="green", text="Sync Complete")
#         except Exception as e:
#             self.log(f"❌ Source Machine Error: {e}")
#         finally:
#             self.sync_button.configure(state="normal", text="Run Smart Sync")

# if __name__ == "__main__":
#     app = ZKSyncApp()
#     app.mainloop()



























import customtkinter as ctk
from zk import ZK
import threading
import time
import os
import pickle
from tkinter import filedialog, messagebox

# --- UI THEME CONFIGURATION ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ZKProSuite(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ZK Biometric Professional Management Suite")
        self.geometry("850x920")

        # Load Icon
        try:
            if os.path.exists("zkt-syncer-logo.ico"):
                self.iconbitmap("zkt-syncer-logo.ico")
        except: pass

        # --- UI LAYOUT ---
        self.header = ctk.CTkLabel(self, text="ZK Biometric Management Suite", font=("Roboto", 24, "bold"))
        self.header.pack(pady=15)

        # 1. Connection Frame
        self.conn_frame = ctk.CTkFrame(self)
        self.conn_frame.pack(padx=20, pady=5, fill="x")

        self.src_label = ctk.CTkLabel(self.conn_frame, text="Source (Main) Device IP:")
        self.src_label.grid(row=0, column=0, padx=10, pady=5)
        self.src_entry = ctk.CTkEntry(self.conn_frame, width=200)
        self.src_entry.insert(0, "172.172.173.235")
        self.src_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        self.tgt_label = ctk.CTkLabel(self.conn_frame, text="Target Device IPs (Comma Sep):")
        self.tgt_label.grid(row=1, column=0, padx=10, pady=5)
        self.tgt_entry = ctk.CTkEntry(self.conn_frame, width=450)
        self.tgt_entry.insert(0, "172.172.173.234")
        self.tgt_entry.grid(row=1, column=1, padx=10, pady=5)

        # 2. Manual Delete Frame
        self.del_frame = ctk.CTkFrame(self, fg_color="#331a1a")
        self.del_frame.pack(padx=20, pady=10, fill="x")
        
        self.del_label = ctk.CTkLabel(self.del_frame, text="Manual Delete from Main Device:", font=("Roboto", 12, "bold"))
        self.del_label.grid(row=0, column=0, padx=10, pady=10)
        self.del_id_entry = ctk.CTkEntry(self.del_frame, placeholder_text="Enter ID (e.g. 1182)", width=150)
        self.del_id_entry.grid(row=0, column=1, padx=10, pady=10)
        self.del_btn = ctk.CTkButton(self.del_frame, text="Delete User Permanently", fg_color="#7a1f1f", hover_color="#a82828", command=lambda: self.start_task("manual_delete"))
        self.del_btn.grid(row=0, column=2, padx=10, pady=10)

        # 3. Maintenance Tools Frame
        self.maint_frame = ctk.CTkFrame(self, fg_color="#2b2b2b")
        self.maint_frame.pack(padx=20, pady=5, fill="x")
        self.m_label = ctk.CTkLabel(self.maint_frame, text="Device Maintenance (Target IPs):", font=("Roboto", 12, "bold"))
        self.m_label.grid(row=0, column=0, columnspan=4, padx=10, pady=5)

        self.unlock_btn = ctk.CTkButton(self.maint_frame, text="Unlock (Clear Admins)", fg_color="#5a5a5a", width=185, command=lambda: self.start_task("unlock"))
        self.unlock_btn.grid(row=1, column=0, padx=5, pady=10)

        self.reboot_btn = ctk.CTkButton(self.maint_frame, text="Reboot Device", fg_color="#5a5a5a", width=185, command=lambda: self.start_task("reboot"))
        self.reboot_btn.grid(row=1, column=1, padx=5, pady=10)

        self.clear_logs_btn = ctk.CTkButton(self.maint_frame, text="Clear Attendance Logs", fg_color="#d97706", width=185, command=lambda: self.start_task("clear_logs"))
        self.clear_logs_btn.grid(row=1, column=2, padx=5, pady=10)

        self.factory_btn = ctk.CTkButton(self.maint_frame, text="FACTORY RESET", fg_color="#b91c1c", hover_color="#7f1d1d", width=185, command=lambda: self.start_task("factory_reset"))
        self.factory_btn.grid(row=1, column=3, padx=5, pady=10)

        # 4. Settings Switch
        self.mirror_var = ctk.BooleanVar(value=True)
        self.mirror_switch = ctk.CTkSwitch(self, text="Mirror Mode (Delete target users if missing in source)", variable=self.mirror_var)
        self.mirror_switch.pack(padx=25, pady=5, anchor="w")

        # 5. Main Action Buttons
        self.btn_frame = ctk.CTkFrame(self)
        self.btn_frame.pack(padx=20, pady=5, fill="x")

        self.sync_btn = ctk.CTkButton(self.btn_frame, text="Run Fast Delta Sync", fg_color="#1f538d", height=45, command=lambda: self.start_task("sync"))
        self.sync_btn.grid(row=0, column=0, padx=5, pady=10, sticky="ew")

        self.backup_btn = ctk.CTkButton(self.btn_frame, text="Backup Source to File", fg_color="#28a745", hover_color="#218838", height=45, command=lambda: self.start_task("backup"))
        self.backup_btn.grid(row=0, column=1, padx=5, pady=10, sticky="ew")

        self.restore_btn = ctk.CTkButton(self.btn_frame, text="Restore File to Target", fg_color="#dc3545", hover_color="#c82333", height=45, command=lambda: self.start_task("restore"))
        self.restore_btn.grid(row=0, column=2, padx=5, pady=10, sticky="ew")
        self.btn_frame.grid_columnconfigure((0,1,2), weight=1)

        # 6. Log Box
        self.log_box = ctk.CTkTextbox(self, width=810, height=280, state="disabled", font=("Consolas", 12))
        self.log_box.pack(padx=20, pady=10)

        self.status_bar = ctk.CTkLabel(self, text="Ready", text_color="gray")
        self.status_bar.pack(pady=5)

    def log(self, message):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"[{time.strftime('%H:%M:%S')}] {message}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def toggle_ui(self, state):
        btns = [self.sync_btn, self.backup_btn, self.restore_btn, self.del_btn, 
                self.unlock_btn, self.reboot_btn, self.clear_logs_btn, self.factory_btn]
        for b in btns: b.configure(state=state)

    def start_task(self, task_type):
        if task_type == "factory_reset" and not messagebox.askyesno("CONFIRM", "WIPE ALL USERS AND LOGS?"): return
        if task_type == "clear_logs" and not messagebox.askyesno("CONFIRM", "Wipe all attendance logs?"): return
        
        self.toggle_ui("disabled")
        self.status_bar.configure(text=f"Processing {task_type.upper()}...", text_color="yellow")
        threading.Thread(target=self.run_task, args=(task_type,), daemon=True).start()

    def run_task(self, task_type):
        try:
            if task_type == "sync": self.handle_sync()
            elif task_type == "backup": self.handle_backup()
            elif task_type == "restore": self.handle_restore()
            elif task_type == "manual_delete": self.handle_manual_delete()
            else: self.handle_maintenance(task_type)
        except Exception as e: self.log(f"❌ ERROR: {e}")
        finally:
            self.toggle_ui("normal")
            self.status_bar.configure(text="Ready", text_color="gray")

    def handle_manual_delete(self):
        source_ip, user_id = self.src_entry.get().strip(), self.del_id_entry.get().strip()
        if not user_id: return self.log("⚠️ Provide User ID.")
        try:
            zk = ZK(source_ip, port=4370, timeout=5); conn = zk.connect()
            conn.delete_user(user_id=user_id)
            self.log(f"✅ User {user_id} deleted from {source_ip}. Run Sync to update targets.")
            self.del_id_entry.delete(0, 'end'); conn.disconnect()
        except Exception as e: self.log(f"❌ Delete Failed: {e}")

    def handle_maintenance(self, action):
        targets = [ip.strip() for ip in self.tgt_entry.get().split(",") if ip.strip()]
        for ip in targets:
            try:
                self.log(f"🛠️ Maintenance: {action.upper()} on {ip}...")
                zk = ZK(ip, port=4370, timeout=10)
                conn = zk.connect()
                conn.disable_device()

                if action == "unlock":
                    # Manual Unlock: Demote all Admins to Users
                    users = conn.get_users()
                    for u in users:
                        if u.privilege > 0:
                            conn.set_user(uid=u.uid, name=u.name, privilege=0, 
                                          password=u.password, user_id=u.user_id)
                    self.log(f"  ✅ Device Unlocked: All admins demoted on {ip}.")
                
                elif action == "reboot":
                    try:
                        conn.restart()
                        self.log(f"  ✅ Rebooting {ip}...")
                    except:
                        # Restarting often breaks the connection immediately, 
                        # which Python sees as an error, but the machine IS rebooting.
                        self.log(f"  ✅ Reboot command sent to {ip}.")

                elif action == "clear_logs":
                    conn.clear_attendance()
                    self.log(f"  ✅ Attendance logs wiped on {ip}.")

                elif action == "factory_reset":
                    # Manual Factory Reset (Bypassing the concat bug)
                    self.log(f"  🔥 Wiping logs...")
                    conn.clear_attendance()
                    self.log(f"  🔥 Deleting all users...")
                    users = conn.get_users()
                    for u in users:
                        conn.delete_user(user_id=u.user_id)
                    self.log(f"  ✅ FULL FACTORY RESET COMPLETE on {ip}.")

                conn.enable_device()
                conn.disconnect()
            except Exception as e:
                # If error is 'instance are not connected' during reboot, it's actually success
                if action == "reboot" and "not connected" in str(e):
                    self.log(f"  ✅ Rebooting {ip}...")
                else:
                    self.log(f"  ❌ {ip} Error: {e}")

    def handle_sync(self):
        source_ip = self.src_entry.get().strip()
        target_ips = [ip.strip() for ip in self.tgt_entry.get().split(",") if ip.strip()]
        self.log("--- FAST DELTA SYNC ---")
        try:
            zk_src = ZK(source_ip, port=4370, timeout=5); conn_src = zk_src.connect()
            src_users, src_templates = conn_src.get_users(), conn_src.get_templates()
            conn_src.disconnect()
            src_user_map = {u.user_id: u for u in src_users}
            src_temp_map = {}
            for t in src_templates:
                if t.uid not in src_temp_map: src_temp_map[t.uid] = []
                src_temp_map[t.uid].append(t)

            for target_ip in target_ips:
                try:
                    zk_tgt = ZK(target_ip, port=4370, timeout=10); conn_tgt = zk_tgt.connect()
                    tgt_users, tgt_templates = conn_tgt.get_users(), conn_tgt.get_templates()
                    tgt_user_map = {u.user_id: u for u in tgt_users}
                    tgt_f_count = {}
                    u_to_uid = {u.uid: u.user_id for u in tgt_users}
                    for t in tgt_templates:
                        uid = u_to_uid.get(t.uid)
                        if uid: tgt_f_count[uid] = tgt_f_count.get(uid, 0) + 1
                    
                    conn_tgt.disable_device()
                    if self.mirror_var.get():
                        for t_id in list(tgt_user_map.keys()):
                            if t_id not in src_user_map:
                                self.log(f"  🗑️ Removing User {t_id}"); conn_tgt.delete_user(user_id=t_id)

                    added, updated, skipped = 0, 0, 0
                    for s_id, s_u in src_user_map.items():
                        t_u = tgt_user_map.get(s_id); s_f = src_temp_map.get(s_u.uid, [])
                        if not t_u or t_u.name != s_u.name or t_u.privilege != s_u.privilege or len(s_f) != tgt_f_count.get(s_id, 0):
                            conn_tgt.set_user(uid=s_u.uid, name=s_u.name, privilege=s_u.privilege, user_id=s_u.user_id)
                            for f in s_f: conn_tgt.save_user_template(s_u, f)
                            if not t_u: added += 1
                            else: updated += 1
                        else: skipped += 1
                    self.log(f"✅ {target_ip}: {added} added, {updated} updated, {skipped} skipped.")
                    conn_tgt.enable_device(); conn_tgt.disconnect()
                except Exception as e: self.log(f"❌ {target_ip} Sync Error: {e}")
        except Exception as e: self.log(f"❌ Source Error: {e}")

    def handle_backup(self):
        ip = self.src_entry.get().strip()
        try:
            zk = ZK(ip, port=4370, timeout=5); conn = zk.connect()
            data = {'users': conn.get_users(), 'templates': conn.get_templates()}
            file = filedialog.asksaveasfilename(defaultextension=".bak", filetypes=[("ZK Backup", "*.bak")])
            if file:
                with open(file, 'wb') as f: pickle.dump(data, f)
                self.log(f"✅ Backup saved: {len(data['users'])} users.")
            conn.disconnect()
        except Exception as e: self.log(f"❌ Backup Error: {e}")

    def handle_restore(self):
        targets = [ip.strip() for ip in self.tgt_entry.get().split(",") if ip.strip()]
        file = filedialog.askopenfilename(filetypes=[("ZK Backup", "*.bak")])
        if not file: return
        with open(file, 'rb') as f: data = pickle.load(f)
        for ip in targets:
            try:
                zk = ZK(ip, port=4370, timeout=10); conn = zk.connect(); conn.disable_device()
                for u in data['users']: conn.set_user(uid=u.uid, name=u.name, privilege=u.privilege, user_id=u.user_id)
                for t in data['templates']:
                    u_obj = next((u for u in data['users'] if u.uid == t.uid), None)
                    if u_obj: conn.save_user_template(u_obj, t)
                self.log(f"✅ {ip} Restored."); conn.enable_device(); conn.disconnect()
            except Exception as e: self.log(f"❌ {ip} Restore Error: {e}")

if __name__ == "__main__":
    app = ZKProSuite(); app.mainloop()