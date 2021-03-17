import socket 
from threading import Thread, Barrier
import os
from hashlib import sha256
from newClient import NewClient
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"
filename='big.txt'
filesize= os.path.getsize(filename)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '0.0.0.0'
port = 65432
print('Server on')
print ('Waiting for clients')
i= 0
s.bind((host,port))
s.listen()
b = Barrier(1)
pruebas = []
try:
    while True:
        c,addr = s.accept()
        if b.broken:
            b.reset()
        name= f'client{i}.txt'
        i+=1
        prueba =NewClient(c,addr,filename,name,b).start()
        pruebas.append(prueba)
except Exception as e:
    print(e)
    s.close()

