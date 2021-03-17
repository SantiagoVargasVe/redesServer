import socket 
from threading import Thread, Barrier
import os
from hashlib import sha256
from newClient import NewClient
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"
filename='file.txt'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '0.0.0.0'
port = 65432
i= 0
filesend = int(input('Que archivo deseas enviar? \n 1 para 250MB  \n 2 para 150MB\n'))
numClients = int(input('Cuantos clientes simultaneos? \n'))
filename = 'big.txt' if filesend ==1 else 'file.txt'
filesize= os.path.getsize(filename)
print('Server on')
print ('Waiting for clients')
s.bind((host,port))
s.listen()
b = Barrier(numClients)
pruebas = []
try:
    while True:
        c,addr = s.accept()
        if b.broken:
            b.reset()
        name= f'client{i}.txt'
        i+=1
        prueba =NewClient(c,addr,filename,name,filesize,b).start()
        pruebas.append(prueba)
except Exception as e:
    print(e)
    s.close()

