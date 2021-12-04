import socket
import my_cpu_bound_func

def get_server_socket() -> socket.socket:
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_sock.bind(('localhost', 8090))
    server_sock.listen()

    return server_sock


server_socket = get_server_socket()

while True:
    # print('Waiting new connection...')
    client_socket, client_addr = server_socket.accept()
    print(f'Connection has been received from {client_addr[0]}:{client_addr[1]}')
    while True:
        data = str(client_socket.recv(4096))[2:-1]

        if len(data) != 0:
            flag, data = data.split(",")

        if data:
            if flag == '0':
                client_socket.send('Pong'.encode())
            elif flag == '1':
                my_sum = my_cpu_bound_func.strange_amount(data)
                client_socket.send(str(my_sum).encode())
        else:
            print('Client has gone')
            client_socket.close()
            break