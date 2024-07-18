import socket
import backend

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('127.0.0.1', 22000))
serversocket.listen(5) 

print('waiting for players to join')
num_of_players = 0
waiting_players = []
while True:
    connection, address = serversocket.accept()
    buf = connection.recv(1024)
    if len(buf) > 0:
        print(buf, address)
        if buf == b'join':
            num_of_players += 1
            waiting_players.append(address)
        connection.send(buf)
        connection.close()
        if num_of_players >= 2:
            print('starting')
            break

game = backend.GameLoop(num_of_players)
id = 0

for address, player in waiting_players, game.playerList:
    id += 1
    player.id = id
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((address, 10000))
    connection.send('{0:07b}'.format(id).encode())
    connection.close()



# import logging
# import socket
# import sys
# from utils import *

# logger = logging.getLogger()
# addresses = []


# def main(host='0.0.0.0', port=9999):
#     sock = socket.socket(socket.AF_INET, # Internet
#                          socket.SOCK_DGRAM) # UDP
#     sock.bind((host, port))
#     while True:
#         data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
#         logger.info("connection from: %s", addr)
#         addresses.append(addr)
#         if len(addresses) >= 2:
#             logger.info("server - send client info to: %s", addresses[0])
#             sock.sendto(addr_to_msg(addresses[1]), addresses[0])
#             logger.info("server - send client info to: %s", addresses[1])
#             sock.sendto(addr_to_msg(addresses[0]), addresses[1])
#             addresses.pop(1)
#             addresses.pop(0)


# if __name__ == '__main__':
#     logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
#     main(*addr_from_args(sys.argv))