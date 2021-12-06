import socket
import time

SERVER_HOST = 'localhost'
SERVER_PORT = 8090


client_socket = socket.socket()
client_socket.connect((SERVER_HOST, SERVER_PORT))

print('Sending Ping...')
for _ in  range(5):
    client_socket.send('Ping'.encode())
    print('Receiving response...')
    response = client_socket.recv(4096)
    print(f'{response}was received')
    time.sleep(5)

print('Closing connection...')
client_socket.close()