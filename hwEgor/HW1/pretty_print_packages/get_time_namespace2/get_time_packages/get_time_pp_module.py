from datetime import datetime
from get_time_namespace.get_time_unicode_packages.get_time_unicode_module import get_time


def print_time_pretty(unixtime):
    formatted_time = datetime.utcfromtimestamp(unixtime).strftime('%Y-%m-%d %H:%M:%S')
    print(formatted_time)

def main():
    unixtime = get_time()
    print_time_pretty(unixtime)

if __name__ == '__main__':
    main()