# Log4Shell-Detection-System
A real-time detection system for Log4Shell attacks using Python, Regex, and VirusTotal API.

# 🛡️ Log4Shell Detection System (IDS)

A Python-based Intrusion Detection System (IDS) designed to detect and analyze **Log4Shell (CVE-2021-44228)** attacks in real-time.

## 📌 Overview
This project simulates a real-world attack scenario using a **Kali Linux** attacker and a vulnerable **Apache Web Server**. The protection system monitors server logs, detects malicious JNDI payloads, neutralizes evasion techniques, and verifies attacker IP reputation using the **VirusTotal API**.

## 🚀 Features
* **Real-time Monitoring:** Continuously watches `access.log` for suspicious patterns.
* **Anti-Evasion Engine:** Decodes URL-encoded payloads and normalizes obfuscated strings (e.g., `${lower:j}`) to detect sophisticated attacks.
* **Threat Intelligence:** Automatically queries **VirusTotal API** to check if the attacker's domain is known as malicious.
* **Alerting:** Provides immediate console alerts with attack details.

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **Environment:** Apache Web Server (XAMPP), Kali Linux (Attacker)
* **Libraries:** `re` (Regex), `requests` (API), `urllib`
* 
## ⚙️ How to Run
1.  Configure the `LOG_FILE_PATH` in the script to match your Apache access log location.
2.  Add your VirusTotal API Key to the `VT_API_KEY` variable.
3.  Run the script:
    ```bash
    python defender.py
    ```

## ⚠️ Disclaimer
This project is for educational purposes only. Tested in an isolated virtual laboratory.
