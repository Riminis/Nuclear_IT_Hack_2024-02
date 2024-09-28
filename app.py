import json
import pandas as pd
from geopy.distance import geodesic
import psycopg2
from flask import Flask, request, jsonify
import requests

db_config = {
    'dbname': 'qablit79',
    'user': 'qablit79_user',
    'password': 'kPp7GjQFEJLEff1qPXuwOp4BwKPzkUmu',
    'host': 'dpg-crg5qcjv2p9s73a8f8vg-a.oregon-postgres.render.com',
    'port': '5432'
}
app = Flask(__name__)

@app.route('/', methods=['GET'])
def handle_post_1():
    response = {
        "message": "Alive"
    }

    return jsonify(response), 200


@app.route('/passenger_flow_metro', methods=['GET'])
def handle_post():
    data = request.get_json()

    response = {
        "message": "Alive"
    }

    my_location = (data["lng"], data["lst"])

    return jsonify('0'), 200


if __name__ == '__main__':
    app.run(host='localhost', port=4000)
