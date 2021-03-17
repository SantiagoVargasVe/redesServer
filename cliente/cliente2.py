import socket
import os
from hashlib import sha256
from threading import Thread

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server
BUFFER_SIZE = 10420
SEPARATOR = "<SEPARATOR>"
integrity=''

def createClients():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b'Hola')
        filename = s.recv(BUFFER_SIZE)
        integrity = s.recv(BUFFER_SIZE).decode()
        with open(filename,'wb') as f:
            for i in range(64000):
                bytes_read = s.recv(4096)
                f.write(bytes_read)
        with open(filename,'rb') as j:
            sha = j.read()
            security= sha256(sha).hexdigest()
            print(security)
            print(integrity)

        print ('Voy a mandar mensaje')
        if (security == integrity):
            s.sendall(b'Si que somos iguales')
            print('Somos iguales')    
        else:
            print('sad face')
                
        

number_clients = int(input("Cuantos clientes"))

for i in range(0,number_clients):
    Thread(target=createClients).start()
