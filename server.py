import socket 
from threading import Thread, Barrier
import os
from hashlib import sha256
from newClient import NewClient
from datetime import datetime
from os import listdir
from os.path import isfile, join
from datetime import datetime
import pandas as pd 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '0.0.0.0'
port = 65432
i= 0

def joinFiles():
    mypath= 'logs/'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    logs_only = [f'{mypath}{item}' for item in onlyfiles]
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
    combined = pd.concat([pd.read_csv(f, delimiter=';', encoding='UTF-8') for f in logs_only])
    combined.to_csv(f'{dt_string}.csv')

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
except KeyboardInterrupt as e:
    joinFiles()
    s.close()