"""
USB Device Logger
Monitors for new USB device connections and logs them
"""
import subprocess
import time
import os
import sys
from datetime import datetime

# Set UTF-8 output
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "usb_log.txt")

def get_usb_devices():
    """Get currently connected USB devices"""
    try:
        cmd = ['powershell', '-Command', 
               'Get-PnpDevice -Class USB -Status OK | '
               'Select-Object FriendlyName, Manufacturer, Status | '
               'ConvertTo-Json -Compress']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0 and result.stdout.strip():
            import json
            devices = json.loads(result.stdout)
            if isinstance(devices, dict):
                devices = [devices]
            return devices
        return []
    except Exception as e:
        return [{"error": str(e)}]

def log_event(message):
    """Log to file with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")

def monitor_loop(interval=10):
    """Monitor for USB device changes"""
    print("USB Device Logger Started")
    print(f"Checking every {interval} seconds... (Ctrl+C to stop)\n")
    
    known_devices = {d.get("FriendlyName", "Unknown") for d in get_usb_devices()}
    print(f"Initial devices: {len(known_devices)}")
    
    while True:
        time.sleep(interval)
        current_devices = {d.get("FriendlyName", "Unknown") for d in get_usb_devices()}
        
        new = current_devices - known_devices
        if new:
            for device in new:
                msg = f"CONNECTED: {device}"
                print(msg)
                log_event(msg)
        
        removed = known_devices - current_devices
        if removed:
            for device in removed:
                msg = f"DISCONNECTED: {device}"
                print(msg)
                log_event(msg)
        
        known_devices = current_devices

def quick_check():
    """One-time check of USB devices"""
    print("USB Device Check\n" + "="*40)
    devices = get_usb_devices()
    
    if not devices:
        print("No USB devices found")
        return
    
    print(f"Found {len(devices)} USB device(s):\n")
    for i, dev in enumerate(devices, 1):
        name = dev.get("FriendlyName", "Unknown")
        mfr = dev.get("Manufacturer", "N/A")
        status = dev.get("Status", "Unknown")
        print(f"{i}. {name}")
        print(f"   Manufacturer: {mfr}")
        print(f"   Status: {status}")
        print()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--monitor":
        monitor_loop()
    else:
        quick_check()
