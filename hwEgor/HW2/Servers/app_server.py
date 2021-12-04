from flask import Flask, jsonify, request, json
import my_cpu_bound_func

app = Flask(__name__)

cities = {
    1: 'Moscow',
    2: 'NN'
}


@app.route("/")
def main_page():
    return "<p>Welcome to the club</p>"


@app.route('/cities', methods=['GET'])
def get_cities():
    return json.dumps(cities)


@app.route("/post", methods=["POST"])
def post_request():
    #print(request.json["num"])
    if request.json['flag'] == 0:
        return str("Ping")
    elif request.json['flag'] == 1:
        my_sum = my_cpu_bound_func.strange_amount(request.json["num"])
        return str(my_sum)


if __name__ == '__main__':
    app.run()
