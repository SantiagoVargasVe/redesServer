from threading import Thread
from hashlib import sha256
from time import perf_counter
from math import ceil
class NewClient(Thread):
    def __init__ (self, client_socket,addr,filename,name,filesize,barrier):
        Thread.__init__(self)
        self.client_socket = client_socket
        self.addr = addr
        self.filename = filename
        self.name = name
        self.barrier = barrier
        self.filesize = filesize
    

    def run(self):
        try:
            print('Hola')
            self.barrier.wait()
            tic = perf_counter()
            msg = self.client_socket.recvmsg(1024)
            print(self.addr, '>>',msg,'>>', self.name)
            number_bytes = 0
            with open(self.filename,'rb') as f:
                sha= f.read()
                security = sha256(sha).hexdigest()
                data = f'{self.name}<>{security}<>{self.filesize}'
                number_bytes=self.client_socket.send(f'{data}'.encode())
                msg = self.client_socket.recv(1024).decode()
                print(msg)
                if msg:
                    number_bytes+= self.client_socket.sendfile(f,0)
            houston = self.client_socket.recv(1024).decode()
            print(houston)
            self.client_socket.close()
            toc = perf_counter()
            performance= toc - tic
            name_file= self.name[:self.name.index('.')]
            with open(f'logs/{name_file}.csv', 'w+') as j:
                j.write('tiempo;nombre_enviado;cliente;satisfactorio;numbytes;paquetes \n')
                identifier= self.name.replace('client','')
                identifier = identifier.replace('.txt','')
                j.write(f'{performance};{self.name};{identifier};{houston};{number_bytes};{ceil(number_bytes/1024)}\n')
                pass
            
        except Exception as e:
            self.client_socket.close()
            print(e)

        
        
