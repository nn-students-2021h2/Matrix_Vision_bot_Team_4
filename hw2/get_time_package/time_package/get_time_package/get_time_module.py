import sys
import requests
try:
    from time_package.pretty_print_package.pretty_print_module import print_time_pretty
except ModuleNotFoundError:
    pass


def get_time():
    url = 'http://worldtimeapi.org/api/timezone/Europe/Moscow'
    resp = requests.get(url)
    unixtime = resp.json()['unixtime'] # if use get('unixtime') there is no key, use default value
    return unixtime

def print_time(unixtime):
    print(unixtime)

def main():
    unixtime = get_time()
    if 'time_package.pretty_print_package' not in sys.modules:
        print_time(unixtime)
    else:
        print_time_pretty(unixtime)

if __name__ == '__main__':
    main()
