from flask import Flask, request, jsonify

from main import *

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hand():
    response = {
        "message": "Alive"
    }
    return jsonify(response), 200

@app.route('/data_metro_flow', methods=['GET', 'POST'])
def hand_1():
    answer = request.get_json()

    my_location = answer['lng'], answer['lst']

    squre = answer['area']

    type_building = answer['isResidential']

    print('Получены данные')

    people = people_in_building(squre, type_building)
    nearest_station = find_nearest_station(my_location, metro_data)

    response = {
        "data_metro_flow": passenger_flow_metro(people, coord_centre, nearest_station),
        "data_road": get_nearby_roads_capacity(my_location, coord_centre, people)
    }
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='localhost', port=4000)
