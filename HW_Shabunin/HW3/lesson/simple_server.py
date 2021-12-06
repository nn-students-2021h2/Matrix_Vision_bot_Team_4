import socket

def get_server_socket() -> socket.socket:
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_sock.bind(('localhost', 8090))
    server_sock.listen()

    return server_sock

server_socket = get_server_socket()


while True:
    print('Waiting new connection...')
    client_socket, client_addr = server_socket.accept()
    print(f'Connection has been received from {client_addr[0]}:{client_addr[1]}')

    while True:
        data = client_socket.recv(4096)
        print(f'Received: {data}')

        if data:
            print('Sending Pong to client')
            client_socket.send('Pong'.encode())
        else:
            print('Client has done.')
            client_socket.close()
            break