#import flask
from flask import Flask
from flask import json
import logging

from cpu_bound_task import fib

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
cities = {0:'Moscow', 1:"NN"}


@app.route("/")
def main_page():
    return "<p>Welcome</p>"


@app.route('/cities', methods=['GET'])
def get_cities():
    return json.dumps(cities)


@app.route('/fib', methods=['GET'])
def get_fib():
    return json.dumps(fib(10000))


if __name__ == '__main__':
    app.run(0)