import selectors
import socket

from cpu_bound_task import fib


CLIENT_IS_ALIVE = 0
CLIENT_DISCONNECTED = 1
log = False
selector = selectors.DefaultSelector()


def accept_connection(server_sock: socket.socket):
    print("Accept")
    client_socket, addr = server_sock.accept()

    selector.register(
        fileobj=client_socket,
        events=selectors.EVENT_READ,
        data=send_message
    )


def send_message(client_sock: socket.socket) -> None:
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
        print('Client has gone. Close.')
        selector.unregister(client_sock)
        client_sock.close()
        return CLIENT_DISCONNECTED



def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 8090))
    server_socket.listen()

    selector.register(
        fileobj=server_socket,
        events=selectors.EVENT_READ,
        data=accept_connection
    )


def event_loop():
    count = 0
    while True:
        events = selector.select() # key, events (bit mask read or write)
        for key, _ in events: # key has fileobj, events, data
            callback = key.data
            ret_status = callback(key.fileobj)
            if ret_status == CLIENT_DISCONNECTED:
                print(f"Got {count} queries.")
                count = 0
            else:
                count += 1



if __name__ == '__main__':
    server()
    event_loop()
