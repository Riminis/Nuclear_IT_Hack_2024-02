from flask import Flask, request, jsonify
from main import *


app = Flask(__name__)

@app.route('/', methods=['GET'])
def hand():
    response = {
        "message": "Alive"
    }
    return jsonify(response), 200

@app.route('/data_metro_flow', methods=['GET'])
def hand_1():
    people = people_in_building(test_floors, test_square, test_type_building)
    nearest_station = find_nearest_station(my_location, metro_data)

    response = {
        "data": passenger_flow_metro(people, coord_centre, nearest_station)
    }
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='localhost', port=4000)
