import selectors
import socket
import my_cpu_bound_func

selector = selectors.DefaultSelector()


def server():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(('localhost', 8090))
    server_sock.listen()

    selector.register(
        fileobj=server_sock,
        events=selectors.EVENT_READ,
        data=accept_connection
    )


to_monitor = []


def accept_connection(server_sock: socket.socket) -> None:
    client_socket, client_addr = server_sock.accept()
    print(f'Connection has been received from {client_addr[0]}:{client_addr[1]}')
    selector.register(
        fileobj=client_socket,
        events=selectors.EVENT_READ,
        data=send_message
    )


def send_message(client_sock: socket.socket) -> None:
    data = str(client_sock.recv(4096))[2:-1]

    if len(data) != 0:
        flag, data = data.split(",")
    # print(f'Received: {request}')

    if data:
        if flag == '0':
            client_sock.send('Pong'.encode())
        elif flag == '1':
            my_sum = my_cpu_bound_func.strange_amount(data)
            client_sock.send(str(my_sum).encode())
    else:
        print('Client has gone. Closing client socket...')
        selector.unregister(client_sock)
        client_sock.close()


def event_loop():
    while True:
        events = selector.select()  # key, events (bit mask read or write)
        for key, _ in events:  # key has fileobj, events, data
            callback_function = key.data
            callback_function(key.fileobj)


if __name__ == '__main__':
    server()
    event_loop()
