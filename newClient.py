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
            
            with open(self.filename,'rb') as f:

                act = f.read(4096)
                while act:
                    self.client_socket.sendall(act)
                    confirm = self.client_socket.recv(2048)
                    print(confirm.decode())
                    sha_act = sha256(act).hexdigest()
                    while not sha_act == confirm.decode():
                        print('No son iguales')
                        self.client_socket.sendall(b'INCORRECT')
                        self.client_socket.sendall(act)
                        confirm= self.client_socket.recv(2048)
                    print('Si somos iguales')
                    self.client_socket.sendall(b'CORRECT')
                    act = f.read(4096)

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
            with open(f'logs/{name_file}.txt', 'w+') as j:
                j.write(f'time:{performance} \n')
                j.write(f'nombre_enviado:{self.name}\n')
                identifier= self.name.replace('client','')
                identifier = identifier.replace('.txt','')
                j.write(f'cliente:{identifier}\n')
                j.write(f'satisfactorio:{houston}\n')
                j.write(f'tiempo:{performance}ns\n')
                j.write(f'numbytes:{number_bytes}\n')
                j.write(f'num_paquetes:{ceil(number_bytes/1024)}')

                pass
            
        except Exception as e:
            self.client_socket.close()
            print(e)

        
        
