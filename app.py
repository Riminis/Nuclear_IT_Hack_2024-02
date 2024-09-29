from flask import Flask, request, jsonify
from data import *


app = Flask(__name__)

@app.route('/', methods=['GET'])
def hand():
    response = {
        "message": "Alive"
    }
    return jsonify(response), 200

@app.route('/data_metro_flow', methods=['GET'])
def hand_1():
    response = {
        "data": data
    }
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='localhost', port=4000)
