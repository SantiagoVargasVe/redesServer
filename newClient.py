from threading import Thread
from hashlib import sha256
class NewClient(Thread):
    def __init__ (self, client_socket,addr,filename,name,filesize,barrier):
        Thread.__init__(self)
        self.client_socket = client_socket
        self.addr = addr
        self.filename = filename
        self.name = name
        self.barrier = barrier
    

    def run(self):
        try:
            self.barrier.wait()
            msg = self.client_socket.recvmsg(1024)
            print(self.addr, '>>',msg,'>>', self.name)
            number_bytes = 0
            number_bytes += self.client_socket.send(f'{self.name}'.encode())
            with open(self.filename,'rb') as f:
                sha= f.read()
                security = sha256(sha).hexdigest()
                print(security.encode())
                number_bytes += self.client_socket.send(security.encode())
                number_bytes+= self.client_socket.sendfile(f,0)
            

            msg = self.client_socket.recv(1024)
            print(msg)
            self.client_socket.close()
        except Exception as e:
            print(e)

        
        
