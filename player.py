## PLAYER ##


import socket


while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('100.88.125.61', 10000))
    data = input()
    if data == '':
        s.close()
        continue
    s.send(data.encode())
    data = s.recv(64).decode()
    print(data)
    s.close()
    if data == 'exit ack':
        break