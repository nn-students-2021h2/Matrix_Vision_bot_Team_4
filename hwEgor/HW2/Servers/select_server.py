import socket
from select import select
import my_cpu_bound_func


def get_server_socket():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(('localhost', 8090))
    server_sock.listen()

    return server_sock


to_monitor = []


def accept_connection(server_sock: socket.socket) -> None:
    client_socket, client_addr = server_sock.accept()
    print(f'Connection has been received from {client_addr[0]}:{client_addr[1]}')
    to_monitor.append(client_socket)


def send_message(client_sock: socket.socket) -> None:
    data = str(client_sock.recv(4096))[2:-1]

    if len(data) != 0:
        flag, data = data.split(",")

    if data:
        if flag == '0':
            client_sock.send('Pong'.encode())
        elif flag == '1':
            my_sum = my_cpu_bound_func.strange_amount(data)
            client_sock.send(str(my_sum).encode())
    else:
        print('Client has gone. Closing client socket...')
        to_monitor.remove(client_sock)
        client_sock.close()


def event_loop():
    while True:
        # readable, writable, errors
        ready_to_read, _, _ = select(to_monitor, [], [])
        for sock in ready_to_read:
            if sock == server_socket:
                accept_connection(sock)
            else:
                send_message(sock)


if __name__ == '__main__':
    server_socket = get_server_socket()
    to_monitor.append(server_socket)
    event_loop()
