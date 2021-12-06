import socket

from cpu_bound_task import fib

log = False


def get_server_socket() -> socket.socket:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind(('localhost', 8090))
    server_socket.listen()

    return server_socket


def main():
    server_socket = get_server_socket()
    while True:
        print('Waiting for new connection..')
        client_socket, client_addr = server_socket.accept()
        print(f'Connection has been received from {client_addr[0]}:{client_addr[1]}')
        count = 0
        while True:
            data = client_socket.recv(4096)
            if log: 
                print(f'Received: {data}')
            if data:
                data = data.decode()
                if data[:3] == 'cpu':
                    data = str(fib(int(data[3:])))
                else:
                    data = 'Pong'
                client_socket.send(data.encode())
                if log: 
                    print(f'Sending {data} to client')
                count += 1
            else:
                print('Client has gone. Close.')
                client_socket.close()
                break
        print(f'Got {count} queries')


if __name__ == '__main__':
    main()