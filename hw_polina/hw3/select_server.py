import socket
import select

from cpu_bound_task import fib


log = False
CLIENT_IS_ALIVE = 0
CLIENT_DISCONNECTED = 1


def get_server_socket() -> socket.socket:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind(('localhost', 8090))
    server_socket.listen()

    return server_socket


to_monitor = []
server_socket = get_server_socket()


def accept_connection(server_socket):
    client_socket, client_addr = server_socket.accept()
    to_monitor.append(client_socket)


def send_message(client_sock):
    data = client_sock.recv(4096)
    if log:
        print(f'Received: {data}')

    if data:
        data = data.decode()
        if data[:3] == 'cpu':
            data = str(fib(int(data[3:])))
        else:
            data = 'Pong'
        client_sock.send(data.encode())
        if log: 
            print(f'Sending {data} to client')
        return CLIENT_IS_ALIVE
    else:
        if log:
            print('Client has gone. Close.')
        to_monitor.remove(client_sock)
        client_sock.close()
        return CLIENT_DISCONNECTED


def event_loop():
    count = 0
    while True:
        #readabale, writable, errors
        ready_to_read, _, _ = select.select(to_monitor, [], [])
        for sock in ready_to_read:
            if sock is server_socket:
                accept_connection(sock)
            else:
                ret_status = send_message(sock)
                if ret_status == CLIENT_DISCONNECTED:
                    print(f"Got {count} queries.")
                    count = 0
                else:
                    count += 1

if __name__ == '__main__':
    to_monitor.append(server_socket)
    event_loop()
