import time
import re
import os
import requests 
import ctypes # For Windows Pop-up alerts
import subprocess # For running system commands (Firewall)
from urllib.parse import unquote

# --- Configuration ---
LOG_FILE_PATH = r'C:\xampp\apache\logs\access.log'
LOG4J_PATTERN = r'\$\{jndi:(?:ldap|rmi|dns)://([^/]+)/'

# VirusTotal API Key
VT_API_KEY = "MY_API"

def block_ip_in_firewall(ip_address):
    """
    Executes a Windows command to block an IP address using the built-in Firewall.
    WARNING: This script must be run as Administrator for this to work.
    """
    rule_name = f"Log4Shell_Block_{ip_address}"
    
    # The command to add a blocking rule
    # dir=in (Block incoming traffic) | action=block (Drop packets)
    command = f'netsh advfirewall firewall add rule name="{rule_name}" dir=in action=block remoteip={ip_address}'
    
    print(f"      [X] ATTEMPTING TO BLOCK IP: {ip_address}...")
    
    try:
        # Run the command silently in the background
        subprocess.run(command, shell=True, check=True)
        print(f"      [V] SUCCESS! IP {ip_address} has been blocked in Windows Firewall.")
        return True
    except Exception as e:
        print(f"      [!] FAILED to block IP. Are you running as Admin? Error: {e}")
        return False

def show_windows_alert(title, message):
    """
    Displays a native Windows pop-up alert (Topmost).
    """
    try:
        # 0x10 = Critical Icon, 0x40000 = Top Most window
        ctypes.windll.user32.MessageBoxW(0, message, title, 0x10 | 0x40000)
    except Exception as e:
        print(f"Error showing popup: {e}")

def normalize_log_line(line):
    """
    Cleans up evasion techniques (URL encoding, ${lower:x}).
    """
    try:
        line = unquote(line)
    except:
        pass
    line = re.sub(r'\$\{(?:lower|upper):(\w)\}', r'\1', line, flags=re.IGNORECASE)
    return line

def check_virustotal(domain):
    print(f"      [?] Querying VirusTotal for: {domain}...")
    url = f"https://www.virustotal.com/api/v3/domains/{domain}"
    headers = {"x-apikey": VT_API_KEY}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            stats = response.json()['data']['attributes']['last_analysis_stats']
            malicious_count = stats['malicious']
            if malicious_count > 0:
                return f"DANGEROUS! ({malicious_count} vendors flagged this)"
            return "Clean"
        elif response.status_code == 404:
            return "Unknown Domain"
        return f"Error ({response.status_code})"
    except Exception as e:
        return f"Connection Error: {e}"

# --- Main Program ---
print("[*] Starting DEFENDER 7.0 (IPS - Active Blocking Mode)...")
print("[!] MAKE SURE YOU ARE RUNNING AS ADMINISTRATOR!")

if not os.path.exists(LOG_FILE_PATH):
    print("Error: Log file not found.")
    exit()

try:
    f = open(LOG_FILE_PATH, 'r')
    f.seek(0, os.SEEK_END)
except Exception as e:
    print(f"Error opening file: {e}")
    exit()

print(f"[*] Monitoring active log: {LOG_FILE_PATH}")
print("[*] Waiting for attacks...")

while True:
    original_line = f.readline()
    if not original_line:
        time.sleep(0.1)
        continue
    
    clean_line = normalize_log_line(original_line)
    
    # --- Detection Logic ---
    if "${jndi:" in clean_line:
        print(f"\n[!!!] ALERT: Sophisticated Log4Shell Attack Detected!")
        
        # 1. Extract Attacker IP (Usually the first word in the log line)
        attacker_ip = original_line.split(' ')[0]
        
        # 2. Extract Malicious Payload Domain
        domain = "Unknown"
        match = re.search(LOG4J_PATTERN, clean_line)
        vt_result = "N/A"
        
        if match:
            domain = match.group(1)
            print(f"      Attacker IP: {attacker_ip}")
            print(f"      Payload Domain: {domain}")
            
            # 3. Check Reputation
            vt_result = check_virustotal(domain)
            print(f"      VirusTotal Analysis: {vt_result}")
        
        # 4. ACTIVE DEFENSE: Block the Attacker!
        # We block the IP extracted from the log
        block_success = block_ip_in_firewall(attacker_ip)
        
        status_msg = "BLOCKED" if block_success else "FAILED TO BLOCK"

        # 5. Show Pop-up Alert
        alert_title = "🚨 INTRUSION PREVENTED 🚨"
        alert_body = (f"Log4Shell Attack Detected!\n\n"
                      f"Source IP: {attacker_ip}\n"
                      f"Payload: {domain}\n"
                      f"VirusTotal: {vt_result}\n\n"
                      f"Action Taken: firewall Rule Added ({status_msg})")
        
        show_windows_alert(alert_title, alert_body)
