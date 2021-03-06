import socket
import os

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Hello, world')
    data = s.recv(BUFFER_SIZE).decode()
    filename , filesize = data.split(SEPARATOR)
    filename = os.path.basename(filename)
    filesize = int(filesize)

    with open(filename,'wb') as f:
        while True:
            bytes_read = s.recv(BUFFER_SIZE)
            if not bytes_read:
                print('Voy a salir  ')
                break
            f.write(bytes_read)

print('Received', repr(data))