import socket 
from threading import Thread, Barrier
import os
from hashlib import sha256
from newClient import NewClient
from datetime import datetime
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '0.0.0.0'
port = 65432
i= 0
numClients = int(input('Cuantos clientes simultaneos? \n'))
# filename = 'big.txt' if filesend ==1 else 'file.txt'
filename = input ('Escriba el nombre del archivo que sea enviar \n Ejemplo: prueba.txt \n')
extension= filename[filename.index('.'):]
filesize= os.path.getsize(filename)
print('Server on')
print ('Waiting for clients')
s.bind((host,port))
s.listen(25)
b = Barrier(numClients)
pruebas = []
try:
    while True:
        c,addr = s.accept()
        if b.broken:
            b.reset()
        name= f'client{i}{extension}'
        i+=1
        prueba =NewClient(c,addr,filename,name,filesize,b).start()
        pruebas.append(prueba)
except Exception as e:
    print(e)
    s.close()