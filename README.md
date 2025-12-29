# 🛡️ Log4Shell Defender (IDS & IPS)

A Python-based Intrusion Prevention System (IPS) designed to **detect, analyze, and actively block** Log4Shell (CVE-2021-44228) attacks in real-time.

## 📌 Overview
This project simulates a full defense cycle against a cyber attack. Using a **Kali Linux** attacker and a vulnerable **Apache Web Server**, the system monitors logs for malicious JNDI payloads. Upon detection, it performs deep analysis using **VirusTotal**, triggers immediate desktop alerts, and **automatically blocks the attacker's IP** using the Windows Firewall.

## 🚀 Features
* **Active Blocking (IPS):** Automatically executes firewall rules (`netsh`) to block the attacker's IP address immediately upon detection.
* **Real-time Monitoring:** Continuously watches `access.log` for suspicious patterns.
* **Anti-Evasion Engine:** Decodes URL-encoded payloads and normalizes obfuscated strings (e.g., `${lower:j}`) to detect sophisticated attacks.
* **Threat Intelligence:** Queries **VirusTotal API** to verify attacker reputation.
* **Desktop Alerts:** Triggers a native Windows Pop-up warning (using `ctypes`) to alert the SOC analyst.

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **Core Libraries:** `re` (Regex), `requests` (API), `subprocess` (System Commands), `ctypes` (Windows API).
* **Security Tools:** Windows Defender Firewall, VirusTotal API.
* **Environment:** Apache Web Server (XAMPP), Kali Linux (Attacker).

## ⚙️ How to Run
⚠️ **Important:** This script requires Administrator privileges to manage Firewall rules.

1.  Configure the `LOG_FILE_PATH` in the script to match your Apache access log location.
2.  Add your VirusTotal API Key to the `VT_API_KEY` variable.
3.  Install dependencies:
    ```bash
    pip install requests
    ```
4.  Open CMD / PowerShell as **Administrator** and run:
    ```bash
    python defender.py
    ```

## 📸 Screenshots
![LOG4SHELL7](https://github.com/user-attachments/assets/9a714551-4960-4d01-90ae-731ddcbe8399)
![LOG4SHELL6](https://github.com/user-attachments/assets/0fa8c185-3c61-4a8c-a164-e8654a656833)
![LOG4SHELL5](https://github.com/user-attachments/assets/326b2a66-6679-40c5-ba2a-1b1aaff17aca)
![LOG4SHELL4](https://github.com/user-attachments/assets/167a5d8b-e68c-4e6f-9004-e99aa8858bd2)
![LOG4SHELL3](https://github.com/user-attachments/assets/cabd037f-9754-41c4-9d8b-8d9bab196968)
![LOG4SHELL2](https://github.com/user-attachments/assets/04d7a02f-6888-4357-8597-1c07db65fc29)
![LOG4SHELL1](https://github.com/user-attachments/assets/4377388b-298c-495b-b0ab-e0e9458826e6)

## ⚠️ Disclaimer
This project is for educational purposes only. Tested in an isolated virtual laboratory.!
