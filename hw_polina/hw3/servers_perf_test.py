import socket
from time import perf_counter
from typing import Callable
import requests


def query_socket_server(socket_client : socket.socket, data : str) -> None:
    socket_client.send(str(data).encode())
    response = socket_client.recv(4096)

def query_http_server():
    res = requests.get('http://127.0.0.1:5000/cities')

def query_http_server_cpu_bound():
    res = requests.get('http://127.0.0.1:5000/fib')



def test_pipeline(query : Callable, niter : int = 1000) -> float:
    start_time = perf_counter()
    for _ in range(niter):
        query()
    duration_sec = (perf_counter() - start_time)
    return duration_sec, niter / duration_sec


def test_socket_server(data, niter : int) -> None:
    SERVER_HOST = 'localhost'
    SERVER_PORT = 8090
    socket_client = socket.socket()
    socket_client.connect((SERVER_HOST, SERVER_PORT))
    duration, rps = test_pipeline(lambda: query_socket_server(socket_client, data), niter)
    socket_client.close()
    return duration, rps


def main():
    duration, rps = test_socket_server("cpu10000", 10)
    print(f'Simple/select/selector socket server: {rps:.2f} RPS, total time {duration:.2f} sec.')
    duration, rps = test_pipeline(query_http_server_cpu_bound, 1)
    print(f'HTTP server: {rps:.2f} RPS, total time {duration:.2f} sec.')



if __name__ == '__main__':
    main()