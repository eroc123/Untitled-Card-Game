import socket

server = '127.0.0.1'
port = 10000
sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_STREAM) 
sock.connect((server, port))
sock.sendall('join'.encode())
print(sock.recv(1024))
sock.close()

sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_STREAM) 
sock.connect((server, port))
while True:
    data = sock.recv(1024)
    if data: print(data)
