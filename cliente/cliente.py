import socket
import os
from hashlib import sha256
from threading import Thread
import math
from time import perf_counter_ns
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server
integrity=''

def createClients(numConexiones):
    namelog = ''
    performance = ''
    filename= ''
    filesize = ''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        tic = perf_counter_ns()
        s.connect((HOST, PORT))
        s.sendall(b'Hola')
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
        num_iterations= math.ceil(filesize/4096)
        s.sendall('RECV_DATA'.encode())
        with open(f'archivosRecibidos/{namelog}-Prueba-{numConexiones}{extension}','wb') as f:
            for i in range(num_iterations):
                bytes_read = s.recv(4096)
                f.write(bytes_read)
        with open(f'archivosRecibidos/{namelog}-Prueba-{numConexiones}{extension}','rb') as j:
            sha = j.read()
            security= sha256(sha).hexdigest()
        
            print(security)
            print(integrity)

        print ('Voy a mandar mensaje')
        if (security == integrity):
            s.sendall(b'SUCCESS')
            check_integrity = True
            print('Somos iguales')    
        else:
            s.sendall(b'ERROR')
            check_integrity = False
        toc = perf_counter_ns()
        performance = toc - tic 
    with open(f'{namelog}.txt','w+') as n:
        n.write(f'nombre_archivo:{filename}\n')
        n.write(f'tamaño_archivo:{filesize}')
        n.write(f'nombre_cliente:{namelog}\n')
        n.write(f'Entrega_exitosa:{check_integrity}\n')
        n.write(f'Tiempo:{performance}')

        

number_clients = int(input("Cuantos clientes"))

for i in range(0,number_clients):
    Thread(target=createClients, args=(number_clients,)).start()
