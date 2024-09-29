from flask import Flask, request, jsonify
from input import *

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hand():
    response = {
        "message": "Alive"
    }
    return jsonify(response), 200

@app.route('/data_metro_flow', methods=['GET'])
def hand():
    response = {
        "data": data_metro_flow
    }
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='localhost', port=4000)
