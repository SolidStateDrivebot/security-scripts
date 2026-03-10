# Security Scripts for Windows

A collection of security monitoring scripts for Windows systems.

## Scripts

### 1. Failed Login Watcher (`failed_login_watcher.py`)
Monitors Windows Security event log for failed login attempts and detects brute force attacks.

**Features:**
- Checks last hour for failed login events (Event ID 4625)
- Extracts source IP addresses from login failures
- Detects suspicious patterns (5+ attempts from same IP)
- Alerts on account brute force (10+ attempts)

**Usage:**
```bash
python failed_login_watcher.py
```

**Requirements:**
- Windows OS
- PowerShell
- Python 3.x

---

### 2. USB Device Logger (`usb_device_logger.py`)
Monitors USB device connections and disconnections in real-time.

**Features:**
- Lists currently connected USB devices
- Real-time monitoring mode
- Logs all events to usb_log.txt
- Displays device name, manufacturer, and status

**Usage:**
```bash
# Quick check of current USB devices
python usb_device_logger.py

# Continuous monitoring (Ctrl+C to stop)
python usb_device_logger.py --monitor
```

**Requirements:**
- Windows OS
- PowerShell
- Python 3.x

---

## Installation

1. Clone this repository or download the scripts
2. Ensure Python 3.x is installed
3. Run scripts from command line

**Note:** These scripts require administrator privileges for some operations.

---

## License

MIT License - Feel free to use and modify for your needs.
