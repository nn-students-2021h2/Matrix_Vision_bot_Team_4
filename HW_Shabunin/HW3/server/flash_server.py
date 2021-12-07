from flask import Flask
import cpu_operations

app = Flask(__name__)


@app.route("/")
def main_page():
    return "<h1>App - works!</h1>"


@app.route("/test_message", methods=['GET'])
def get_fib():
    return "test_message"


@app.route("/factorial6", methods=['GET'])
def get_factorial():
    return str(cpu_operations.factorial(6))


if __name__ == "__main__":
    app.run(debug=True)