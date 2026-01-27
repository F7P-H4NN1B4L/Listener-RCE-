#!/usr/bin/python3
"""
Simple listener script
Python 3.8+
"""

import optparse
import base64
import socket
import json


def get_arguments():
    """Get user supplied arguments from terminal."""
    parser = optparse.OptionParser()

    parser.add_option('-l', '--local', dest='local_ip', help='Listener IP')
    parser.add_option('-p', '--port', dest='port', type=int, help='Listener port')

    (options, arguments) = parser.parse_args()
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
        while True:
            command = input(">> ")

            self.reliable_send({"cmd": command})

            if command == "exit":
                self.connection.close()
                break

            result = self.reliable_receive()
            print(result.get("output", ""))


listener = Listener(options.local_ip, options.port)
listener.run()