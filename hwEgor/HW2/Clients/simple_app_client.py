import requests
import time
import statistics

count_ping_operation = 500
counter_for_mean = 10
use_cpu_bound = 1  # 0-not using a cpu_bound, 1-using a cpu_bound


def my_client():
    start_time = time.time()

    url = "http://127.0.0.1:5000/post"

    for i in range(count_ping_operation):
        post = requests.post(url, json={'flag': use_cpu_bound, "num": i})
    program_execution_time = count_ping_operation / (time.time() - start_time)
    return program_execution_time


def main():
    time_list = []

    for i in range(counter_for_mean):
        time_list.append(my_client())
    print(statistics.mean(time_list), "operation per second")


if __name__ == '__main__':
    main()
