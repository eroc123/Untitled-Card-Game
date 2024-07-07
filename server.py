import socket
import backend

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('127.0.0.1', 10000))
serversocket.listen(5) 

while True:
    connection, address = serversocket.accept()
    buf = connection.recv(64)
    if len(buf) > 0:
        print(buf, address)
        connection.sendall(buf + b' ack')
        if buf == b'exit':
            break