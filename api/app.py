import json
import pandas as pd
from geopy.distance import geodesic
import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def handler():

    response = {
        "message": "Alive"
    }

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='localhost', port=4000)
