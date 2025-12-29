import time
import re
import os
import requests 
from urllib.parse import unquote # Tool to decode URL characters (like %20, %7B)

# --- Configuration ---
LOG_FILE_PATH = r'C:\xampp\apache\logs\access.log'

# Regex to detect the Log4j payload (looks for ${jndi:...)
LOG4J_PATTERN = r'\$\{jndi:(?:ldap|rmi|dns)://([^/]+)/'

# VirusTotal API Key
VT_API_KEY = "MY_API"
def normalize_log_line(line):
    """
    Cleans up the log line to remove attacker disguises (Evasion techniques).
    """
    # Step 1: URL Decode
    # Converts encoded characters like '%7B' back to '{'.
    # This ensures attackers can't hide by encoding their payload.
    try:
        line = unquote(line)
    except:
        pass # If decoding fails, just ignore it

    # Step 2: Handle Log4j specific evasion (e.g., ${lower:j})
    # This creates a "clean" version of the line where ${lower:j} becomes 'j'.
    # Regex logic: Find '${lower:X}' and replace it with just 'X'.
    line = re.sub(r'\$\{(?:lower|upper):(\w)\}', r'\1', line, flags=re.IGNORECASE)
    
    return line

def check_virustotal(domain):
    """
    Checks if a domain is malicious using the VirusTotal API.
    """
    print(f"      [?] Querying VirusTotal for: {domain}...")
    url = f"https://www.virustotal.com/api/v3/domains/{domain}"
    headers = {"x-apikey": VT_API_KEY}

    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            # Parse the JSON response to get stats
            stats = response.json()['data']['attributes']['last_analysis_stats']
            malicious_count = stats['malicious']
            
            if malicious_count > 0:
                return f"DANGEROUS! ({malicious_count} vendors flagged this)"
            else:
                return "Clean"
                
        elif response.status_code == 404:
            return "Unknown Domain (Not found in DB)"
        else:
            return f"Error connecting to VT (Status: {response.status_code})"
            
    except Exception as e:
        return f"Connection Error: {e}"

# --- Main Program ---
print("[*] Starting DEFENDER 3.0 (Anti-Evasion Mode)...")

# Check if log file exists
if not os.path.exists(LOG_FILE_PATH):
    print("Error: Log file not found.")
    exit()

try:
    f = open(LOG_FILE_PATH, 'r')
    # Jump to the end of the file to monitor only NEW logs
    f.seek(0, os.SEEK_END)
except Exception as e:
    print(f"Error opening file: {e}")
    exit()

print(f"[*] Monitoring active log: {LOG_FILE_PATH}")

while True:
    original_line = f.readline()
    
    # If no new line, wait and try again
    if not original_line:
        time.sleep(0.1)
        continue
    
    # --- The Core Logic ---
    # Create a normalized (clean) version of the log line for detection
    clean_line = normalize_log_line(original_line)
    
    # Check for the attack signature in the CLEAN line
    if "${jndi:" in clean_line:
        print(f"\n[!!!] ALERT: Sophisticated Log4Shell Attack Detected!")
        
        # Check if the attacker tried to hide (Evasion)
        if original_line != clean_line:
            print(f"      [!] Evasion technique detected and neutralized!")
            print(f"      Original Payload: {original_line.strip()[-50:]}...") 
            print(f"      Decoded Payload:  {clean_line.strip()[-50:]}...")

        # Extract the attacker's domain
        match = re.search(LOG4J_PATTERN, clean_line)
        if match:
            domain = match.group(1)
            print(f"      Attacker Address: {domain}")
            
            # Check reputation with VirusTotal
            vt_result = check_virustotal(domain)
            print(f"      VirusTotal Analysis: {vt_result}")
        else:
            print("      [?] Could not extract domain.")