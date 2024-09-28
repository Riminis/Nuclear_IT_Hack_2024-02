from main import *


#with open('output.json', 'w') as file:
#    json.dump(passenger_flow_metro, file, indent=4)

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

    people = people_in_building(test_floors, test_square, test_type_building)
    nearest_station = find_nearest_station(my_location, metro_data)

    return jsonify(passenger_flow_metro(people, coord_centre, nearest_station)), 200


if __name__ == '__main__':
    app.run(host='localhost', port=4000)
