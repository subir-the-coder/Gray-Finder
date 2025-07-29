# Gray-Finder

Python scripts and tools built for Recon .... Red Teamer

# 🔍 F.I.N.D.E.R - Fast Intelligent Network Domain Enumeration & Recon

<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/d4f2dd8f-7729-48cb-b6c0-2f533cd9612b" />


> ⚠️ Educational and authorized use only. Do not run this tool against targets you do not own or have explicit permission to test.

F.I.N.D.E.R is a powerful, multi-threaded reconnaissance and domain enumeration tool crafted in **Python** on **Parrot OS**. It is designed to automate the process of identifying subdomains, scanning ports, detecting WAF/CDN presence, and gathering WHOIS information — making it an ideal utility for penetration testers, ethical hackers, and bug bounty hunters.

---

## 🚀 Features

- 🌐 **Subdomain Enumeration** (Brute-force & Passive)
- 🧠 **Multithreaded Execution** with `ThreadPoolExecutor` for speed
- 🔒 **Login Page Detection** for brute-force targeting
- 🧱 **CDN / WAF Detection**
- 🛠 **Port Scanning** using raw socket
- 📦 **WHOIS Information Extraction**
- ⚠️ **Subdomain Takeover Detection** (CNAME to dead services)
- 🎨 **Colorized CLI Output** via `colorama`
- 🩸 **Bloody ASCII Banner Lines** with `pyfiglet`
- 📁 **All results saved to `found.txt`**

---

## 🧰 Dependencies

F.I.N.D.E.R requires Python 3.8+ and the following Python libraries:

### Install the dependencies:

colorama
pyfiglet
requests
dnspython
python-whois

**Usage**
chmod +x finder.py
./finder.py -d example.com -t 100

| Flag | Description                      |
| ---- | -------------------------------- |
| `-d` | Target domain to scan            |
| `-t` | Number of threads (default: 100) |

👨‍💻 Author
Subir Sutradhar
🐧 Crafted with ❤️ & CCD on Parrot OS

⚠️ Disclaimer
This tool is intended for educational use and authorized security testing only.
Misuse of this tool can lead to legal consequences.
Always get permission before scanning any system.


**Thank me buying a coffeee if its useful for you**

