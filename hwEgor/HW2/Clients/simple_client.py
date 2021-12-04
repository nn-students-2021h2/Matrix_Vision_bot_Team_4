import socket
import time
import statistics


SERVER_HOST = 'localhost'
SERVER_PORT = 8090


count_ping_operation = 500
counter_for_mean = 10
use_cpu_bound = 0  # 0-not using a cpu_bound, 1-using a cpu_bound


def my_client():
    client_socket = socket.socket()
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    start_time = time.time()

    for i in range(count_ping_operation):
        str_to_send = (str(use_cpu_bound) + ',' + str(i)).encode()
        client_socket.send(str_to_send)
        response = client_socket.recv(4096)
    client_socket.close()

    return count_ping_operation / (time.time() - start_time)


def main():
    time_list = []

    for i in range(counter_for_mean):
        time_list.append(my_client())
    print(statistics.mean(time_list), "operation per second")

if __name__ == "__main__":
    main()
