import sys
from datetime import datetime


def print_time_pretty(unixtime):
    formatted_time = datetime.fromtimestamp(unixtime).strftime('%Y-%m-%d %H:%M:%S')
    print(formatted_time)
