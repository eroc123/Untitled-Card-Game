## SERVER FILE ## 

# networking stuff here
import socket


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('100.88.125.61', 10000))
s.send('hello world')