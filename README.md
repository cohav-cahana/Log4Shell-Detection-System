
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
3. Install dependencies:
   ```bash
   pip install requests
   ```
4. Run the script:
   ```bash
   python defender.py
   ```

## ⚠️ Disclaimer
This project is for educational purposes only. Tested in an isolated virtual laboratory.
![LOG4SHELL5](https://github.com/user-attachments/assets/326b2a66-6679-40c5-ba2a-1b1aaff17aca)
![LOG4SHELL4](https://github.com/user-attachments/assets/167a5d8b-e68c-4e6f-9004-e99aa8858bd2)
![LOG4SHELL3](https://github.com/user-attachments/assets/cabd037f-9754-41c4-9d8b-8d9bab196968)
![LOG4SHELL2](https://github.com/user-attachments/assets/04d7a02f-6888-4357-8597-1c07db65fc29)
![LOG4SHELL1](https://github.com/user-attachments/assets/4377388b-298c-495b-b0ab-e0e9458826e6)
