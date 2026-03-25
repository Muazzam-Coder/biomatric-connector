Biomatric-connector
This is a comprehensive README.md file designed for your professional project. It covers all the modules you've built: the Professional Sync UI, the API Monitoring Service, and the Auto-Typer (Cursor Integration).

ZK Biometric Multi-Tool Suite

A professional Python-based suite for managing, synchronizing, and monitoring ZKTeco biometric attendance devices. This project provides tools for real-time API integration, cross-device data synchronization, and keyboard emulation for legacy software.

🚀 Key Features

Professional Sync UI: Modern Dark-Mode GUI to sync users and fingerprints from one source machine to multiple target machines simultaneously.

Real-time API Monitor: Background service that listens for thumb scans and pushes attendance data to a web server via REST API.

Auto-Typer Integration: Automatically "types" the Employee ID into any active window or text field on your PC as soon as a finger is scanned.

Admin Recovery: Includes logic to demote/unlock devices if an administrator is locked out due to "Illegal Fingerprint" errors.

🛠 Project Structure
attendence-syncer.py (The Multi-Device Syncer)

The core GUI application used to clone users and biometric templates across your network.

Source IP: The "Master" machine containing all registered users.

Target IPs: A comma-separated list (e.g., 172.172.173.234, 172.172.173.232) of machines to be updated.

Tech: Built with CustomTkinter and Threading for a non-blocking UI.

2. api.py (Server Integration)

A headless script designed to run on a server or background PC.

Connects to a specific device (e.g., Floor 1 or Floor 2).

Monitors for new attendance logs.

Sends a JSON payload (employee_id, floor) to a central Django/FastAPI/Node.js server.

3. app.py / main.py (Keyboard Emulator)

Bridges the biometric device with any desktop software (Excel, ERP, Web Forms).

Uses pyautogui to emulate keyboard strokes.

When a user scans their finger, the script instantly types their ID where your cursor is currently blinking.

📦 Installation

Ensure you have Python 3.8+ installed, then install the required dependencies:

code
Bash
download
content_copy
expand_less
pip install pyzk customtkinter requests pyautogui
⚙️ Configuration
Device Settings

Most ZKTeco machines use the following defaults:

Port: 4370

Protocol: UDP/TCP (The scripts handle connection switching automatically).

API Server Settings

In monitor_api.py, update the following variables:

SERVER_IP: The IP of your backend server.

SERVER_PORT: The port your API is listening on.

FLOOR_ID: Unique identifier for the machine location.

📖 Usage
Running the Professional Sync UI
code
Bash
download
content_copy
expand_less
python zk_sync_pro.py

Enter the Source IP.

List Target IPs separated by commas.

Click Start Synchronization.

Running the API Monitor
code
Bash
download
content_copy
expand_less
python monitor_api.py
Running the Auto-Typer

Open the application where you want the ID to appear (e.g., Notepad or a Search bar).

Click inside the text field.

Run the script:

code
Bash
download
content_copy
expand_less
python app.py
⚠️ Technical Troubleshooting & Compatibility
Algorithm Mismatch (9.0 vs 10.0)

If you see "Illegal Fingerprint" after a successful sync, the machines likely have different Fingerprint Algorithm versions.

Check versions using: conn.get_fp_version().

If versions differ (e.g., 9 vs 10), fingerprints cannot be synced via software. Users must be re-registered on the target machine.

Library Bug: 'int' object has no attribute '__dict__'

This suite uses a specific workaround for a known bug in the pyzk library. Fingerprints are synced using the dual-object method:

code
Python
download
content_copy
expand_less
conn_tgt.save_user_template(user_object, template_object)

This ensures compatibility with newer ZK firmware.

🔨 Build to Executable (.exe)

To package the Sync UI for Windows users who don't have Python installed:

code
Bash
download
content_copy
expand_less
pip install pyinstaller
pyinstaller --noconsole --onefile zk_sync_pro.py

The final .exe will be located in the /dist folder.

🤝 Contributing

For updates or feature requests, please contact the lead developer.

Developed by: Muazzam
