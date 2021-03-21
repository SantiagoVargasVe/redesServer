import socket
import os
from hashlib import sha256
from threading import Thread , Barrier
import math
from os import listdir
from os.path import isfile, join
from time import perf_counter_ns
from datetime import datetime
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server
integrity=''

def joinLogs():
    mypath= './'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    onlyfiles.remove('cliente.py')
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
    with open (f'{dt_string}.txt','a+') as logmaster:
        for client_log in onlyfiles:
            with open(client_log,'r') as f:
                logmaster.write(f.read())


def createClients(numConexiones,b):
    namelog = ''
    performance = ''
    filename= ''
    filesize = ''
    numbytes = 0
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        tic = perf_counter_ns()
        s.connect((HOST, PORT))
        numbytes += s.send(b'Hola')
        msg1 = s.recv(1024).decode()
        print(msg1)
        msg1= msg1.split('<>')
        check_integrity=''
        security = ''
        integrity=msg1[1]
        filename= msg1[0]
        extension= filename[filename.index('.'):]
        namelog = filename[:filename.index('.')]
        filesize= int(msg1[2])
        act_count= 0
        num_iterations= math.ceil(filesize/4096)
        numbytes +=s.send('RECV_DATA'.encode())
        with open(f'archivosRecibidos/{namelog}-Prueba-{numConexiones}{extension}','wb') as f:
            while not act_count == filesize:
                bytes_read = s.recv(4096)
                f.write(bytes_read)
                act_count += len(bytes_read)
        with open(f'archivosRecibidos/{namelog}-Prueba-{numConexiones}{extension}','rb') as j:
            sha = j.read()
            security= sha256(sha).hexdigest()
        
            print(security)
            print(integrity)

        print ('Voy a mandar mensaje')
        if (security == integrity):
            numbytes += s.send(b'SUCCESS')
            check_integrity = True
            print('Somos iguales')    
        else:
            numbytes +=s.send(b'ERROR')
            check_integrity = False
        toc = perf_counter_ns()
        performance = toc - tic 
    with open(f'{namelog}.txt','w+') as n:
        n.write(f'nombre_archivo:{filename}\n')
        n.write(f'tamaño_archivo:{filesize}')
        n.write(f'nombre_cliente:{namelog}\n')
        n.write(f'Entrega_exitosa:{check_integrity}\n')
        n.write(f'Tiempo:{performance}ns \n')
        n.write(f'Num_bytes:{numbytes} \n')
        n.write(f'num_paquetes:{2}\n')

    b.wait()

number_clients = int(input("Cuantos clientes"))
b = Barrier(number_clients+1)
for i in range(0,number_clients):
    Thread(target=createClients, args=(number_clients,b,)).start()

b.wait()
joinLogs()

