import socket
import os
from hashlib import sha256
from threading import Thread

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server
BUFFER_SIZE = 1024
SEPARATOR = "<SEPARATOR>"
integrity=''
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Hello, world')
    filename = s.recv(BUFFER_SIZE)
    integrity = s.recv(BUFFER_SIZE).decode()
    print(type(filename))
    with open(filename,'wb') as f:
        while True:
            bytes_read = s.recv(BUFFER_SIZE)
            if not bytes_read:
                print('Voy a salir ')
                break
            f.write(bytes_read)
    s.sendall(b'bye')

print('Received',integrity)