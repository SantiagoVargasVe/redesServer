import socket 
from threading import Thread
import os

BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"
filename='dummy.txt'
filesize= os.path.getsize(filename)
def new_client(client_socket, addr):
    while True:
        msg = client_socket.recv(1024)
        if msg == b'bye':
            break
        print (addr, '>>', msg)
        client_socket.send(f'{filename}{SEPARATOR}{filesize}'.encode())

        with open(filename,'rb') as f:
            while True:
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    print('Entre')
                    # We're donde here
                    break
                client_socket.sendall(bytes_read)
    client_socket.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 65432
print('Server on')
print ('Waiting for clients')

s.bind((host,port))
s.listen()

while True:
    print('hola')
    c,addr = s.accept()
    print('hola2')
    Thread(target=new_client,args=(c,addr)).start()
