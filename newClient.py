from threading import Thread
from hashlib import sha256
class NewClient(Thread):
    def __init__ (self, client_socket,addr,filename,name,barrier):
        Thread.__init__(self)
        self.client_socket = client_socket
        self.addr = addr
        self.filename = filename
        self.name = name
        self.barrier = barrier
        self._return = None
    

    def run(self):
        self.barrier.wait()
        msg = self.client_socket.recvmsg(1024)
        print(msg)
        print(self.addr, '>>',msg)
        number_bytes = 0
        number_bytes += self.client_socket.send(f'{self.name}'.encode())
        with open(self.filename,'rb') as f:
            sha= f.read()
            security = sha256(sha).hexdigest()
            number_bytes += self.client_socket.send(security.encode())
            number_bytes+= self.client_socket.sendfile(f,0)
        
        print(number_bytes)
        self._return = f'hola, soy {self.name}'
        self.client_socket.close()


    def join(self):
        Thread.join(self)
        return self._join()
        
        
