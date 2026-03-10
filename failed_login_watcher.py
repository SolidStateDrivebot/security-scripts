"""
Failed Login Watcher
Monitors Windows Event Log for failed login attempts (brute force detection)
"""
import subprocess
import time
from datetime import datetime
import json
import sys

# Set UTF-8 output
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def get_failed_logins(hours=1):
    """Get failed login attempts from Windows Security log"""
    try:
        cmd = [
            'powershell', '-Command',
            f'Get-WinEvent -FilterHashtable @{{'
            f'LogName="Security";'
            f'StartTime=(Get-Date).AddHours(-{hours});'
            f'ID=4625}} '
            f'-MaxEvents 50 | Select-Object TimeCreated,Message | ConvertTo-Json -Compress'
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0 and result.stdout.strip():
            events = json.loads(result.stdout)
            if isinstance(events, dict):
                events = [events]
            return events
        return []
    except Exception as e:
        return [{"error": str(e)}]

def check_anomalies(events):
    """Check for suspicious patterns"""
    ip_counts = {}
    account_attempts = {}
    
    for event in events:
        msg = event.get("Message", "")
        
        if "Source Network Address:" in msg:
            try:
                ip = msg.split("Source Network Address:")[1].split("\n")[0].strip()
                if ip and ip not in ["-", "127.0.0.1", "::1"]:
                    ip_counts[ip] = ip_counts.get(ip, 0) + 1
            except:
                pass
        
        if "Account Name:" in msg:
            try:
                account = msg.split("Account Name:")[1].split("\n")[0].strip()
                account_attempts[account] = account_attempts.get(account, 0) + 1
            except:
                pass
    
    alerts = []
    
    for ip, count in ip_counts.items():
        if count >= 5:
            alerts.append(f"[ALERT] {count} failed logins from IP: {ip}")
    
    for account, count in account_attempts.items():
        if count >= 10:
            alerts.append(f"[ALERT] {account}: {count} failed attempts")
    
    return alerts

def main():
    print("Failed Login Watcher - Checking last hour...")
    events = get_failed_logins(hours=1)
    
    if not events or all("error" in e for e in events):
        print("No failed login attempts in the last hour")
        return
    
    print(f"Found {len(events)} failed login attempt(s)")
    
    alerts = check_anomalies(events)
    
    if alerts:
        print("\n=== ALERTS ===")
        for alert in alerts:
            print(alert)
    else:
        print("No suspicious patterns detected")

if __name__ == "__main__":
    main()
