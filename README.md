# Cyber-security-and-ethical-hacking-intership-tasks
Welcome to the Cyber Security and Ethical Hacking Internship Toolkit! This repository contains a collection of four specialized security tools developed as part of an intensive internship program. These tools cover fundamental areas of information security, including file integrity monitoring, web application vulnerability scanning, network penetration testing, and advanced cryptography.

> **Disclaimer:** These tools are intended for educational purposes and authorized auditing only. Never run scanners or penetration testing tools against systems or networks you do not have explicit written permission to test.

---

## 📑 Table of Contents
1. [Project Overview](#project-overview)
2. [Prerequisites & Installation](#prerequisites--installation)
3. [Task 1: File Integrity Checker](#task-1-file-integrity-checker)
4. [Task 2: Web Application Vulnerability Scanner](#task-2-web-application-vulnerability-scanner)
5. [Task 3: Penetration Testing Toolkit](#task-3-penetration-testing-toolkit)
6. [Task 4: Advanced Encryption Tool](#task-4-advanced-encryption-tool)
7. [Directory Structure](#directory-structure)

---

## 🚀 Intership Overview
This repository serves as a comprehensive portfolio piece demonstrating practical coding skills applied to cyber security concepts. 
- **Language:** Python 3.x
- **Focus Areas:** Integrity (Hashing), Web Sec (OWASP Top 10), Network Sec (Scanning/Brute-Forcing), Confidentiality (AES Encryption).

---

## 🛠️ Prerequisites & Installation

To run these tools successfully, you will need Python 3 installed on your machine. 

**Step 1:** Clone or download this repository.
**Step 2:** Install the required third-party libraries by running the following command in your terminal:
```bash
pip install requests beautifulsoup4 cryptography
```

---

## 🛡️ Task 1: File Integrity Checker
A security script that calculates cryptographic hashes (SHA-256) of files within a directory to establish a "known-good" baseline. It can then be run at a later time to detect unauthorized modifications, additions, or deletions of files.

### Key Features:
- Uses robust SHA-256 hashing.
- Saves baseline state in a lightweight JSON format.
- Clearly reports exact file changes (Modified, New, or Deleted).

### Detailed Usage:
1. **Generate a Baseline:**
   Before monitoring, create a baseline of a safe directory.
   ```bash
   python file_integrity_checker/integrity_checker.py generate --target ./my_folder --baseline my_baseline.json
   ```
2. **Check for Changes:**
   Run the check command to compare the current state of the directory against your saved baseline.
   ```bash
   python file_integrity_checker/integrity_checker.py check --target ./my_folder --baseline my_baseline.json
   ```

---

## 🕸️ Task 2: Web Application Vulnerability Scanner
An automated reconnaissance tool that scans a given web application for common vulnerabilities such as SQL Injection (SQLi) and Cross-Site Scripting (XSS). It automatically scrapes HTML forms and injects payloads to test input sanitization.

### Key Features:
- Identifies and parses all HTML `<form>` elements and inputs.
- Automatically tests common SQLi payloads (e.g., `' OR 1=1--`).
- Automatically tests common XSS payloads (e.g., `<script>alert(1)</script>`).
- Supports both GET and POST requests.

### Detailed Usage:
To scan a specific URL for all supported vulnerabilities:
```bash
python web_vulnerability_scanner/vuln_scanner.py http://testphp.vulnweb.com --scan all
```
*Note: You can also specify `--scan sqli` or `--scan xss` to target a specific vulnerability type.*

---

## ⚔️ Task 3: Penetration Testing Toolkit
A modular, command-line-driven toolkit designed for active penetration testing. It currently bundles a multithreaded port scanner and a dictionary-based FTP brute-forcer.

### Key Features:
- **Port Scanner:** Uses Python's `socket` and `threading` libraries to rapidly scan thousands of TCP ports to identify open services.
- **FTP Brute-forcer:** Uses Python's built-in `ftplib` to perform dictionary attacks against FTP servers to uncover weak credentials.

### Detailed Usage:
**View the Help Menu:**
```bash
python pentest_toolkit/toolkit.py -h
```

**Run the Port Scanner (e.g., scanning ports 1-1000 on localhost with 50 threads):**
```bash
python pentest_toolkit/toolkit.py portscan 127.0.0.1 -p 1-1000 -t 50
```

**Run the FTP Brute-Forcer:**
```bash
python pentest_toolkit/toolkit.py ftpbrute 192.168.1.10 -u admin -w passwords.txt
```

---

## 🔒 Task 4: Advanced Encryption Tool
A robust, graphical encryption application. It uses the `cryptography` library to implement the highly secure **AES-256 (GCM mode)** algorithm, ensuring military-grade file confidentiality.

### Key Features:
- **GUI-Driven:** Built using `tkinter` for an easy, point-and-click user experience.
- **True AES-256:** Uses a 32-byte key derived from the user's password.
- **PBKDF2 Key Derivation:** Employs SHA-256 hashing with 100,000 iterations and a random salt to defeat rainbow table attacks.
- **Authenticated Encryption:** Uses GCM (Galois/Counter Mode) to ensure both data confidentiality and authenticity.

### Detailed Usage:
Simply launch the graphical interface from your terminal:
```bash
python advanced_file_encryptor/encryptor_gui.py
```
1. Click **Browse** to select the file you want to encrypt or decrypt.
2. Enter your strong password in the text box.
3. Click **Encrypt File** (creates a `.enc` file) or **Decrypt File** (restores the original file).

---

## 📁 Directory Structure
```text
📦 Internship-Tasks
 ┣ 📂 advanced_file_encryptor
 ┃ ┗ 📜 encryptor_gui.py
 ┣ 📂 file_integrity_checker
 ┃ ┗ 📜 integrity_checker.py
 ┣ 📂 pentest_toolkit
 ┃ ┣ 📂 modules
 ┃ ┃ ┣ 📜 __init__.py
 ┃ ┃ ┣ 📜 ftp_bruteforce.py
 ┃ ┃ ┗ 📜 port_scanner.py
 ┃ ┣ 📜 README.md
 ┃ ┗ 📜 toolkit.py
 ┣ 📂 web_vulnerability_scanner
 ┃ ┗ 📜 vuln_scanner.py
 ┗ 📜 README.md
```

