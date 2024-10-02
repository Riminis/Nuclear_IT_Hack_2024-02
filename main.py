from geopy.distance import geodesic
import osmnx as ox
from input import *


def people_in_building(space, space_office, type_building):
    space = int(space)
    space_office = int(space_office)

    people_new_building = -1

    if type_building == 1:
        people_new_building = space / 25 * 0.57
    elif type_building == 2:
        people_new_building = space / 35 * 0.57
    elif type_building == 3:
        people_new_building = space / 45 * 0.57

    people_new_building += int(space_office) / 35 * 0.57

    return people_new_building


def passenger_flow_metro(people_new_building, coord_centre, nearest_station):
    people_flow_out_m = -1
    people_flow_in_m = -1

    people_flow_out_e = -1
    people_flow_in_e = -1

    flow_metro = []

    dis = 0

    for station in nearest_station:
        dis += station[-1]

    nearest_station = sorted(nearest_station, key=lambda row: row[-1])

    n = 0
    
    for row in nearest_station:
        for flow in data_metro_flow:
            if row[0].lower() == flow[0].lower() and row[3][0].lower() == flow[3][0].lower():
                n += 1
                coord_metro = row[1], row[2]
                distance = geodesic(coord_centre, coord_metro).kilometers
                if distance < 5:
                    people_flow_out_m = (0.8 * flow[2]) + 0.7 * 0.8 * people_new_building * (nearest_station[-1 * n][-1] / dis)
                    people_flow_in_m = (0.2 * flow[1]) + 0.7 * 0.2 * people_new_building * (nearest_station[-1 * n][-1] / dis)
                    people_flow_out_e = (0.2 * flow[2]) + 0.7 * 0.2 * people_new_building * (nearest_station[-1 * n][-1] / dis)
                    people_flow_in_e = (0.8 * flow[1]) + 0.7 * 0.8 * people_new_building * (nearest_station[-1 * n][-1] / dis)
                else:
                    people_flow_out_m = (0.2 * flow[2]) + 0.7 * 0.2 * people_new_building * (nearest_station[-1 * n][-1] / dis)
                    people_flow_in_m = (0.8 * flow[1]) + 0.7 * 0.8 * people_new_building * (nearest_station[-1 * n][-1] / dis)
                    people_flow_out_e = (0.8 * flow[2]) + 0.7 * 0.8 * people_new_building * (nearest_station[-1 * n][-1] / dis)
                    people_flow_in_e = (0.2 * flow[1]) + 0.7 * 0.2 * people_new_building * (nearest_station[-1 * n][-1] / dis)
                print(row)
                flow_metro.append({
                    'name': row[0],
                    'Line': row[3],
                    'people_flow_in_m': int(people_flow_in_m),
                    'people_flow_out_m': int(people_flow_out_m),
                    'people_flow_in_e': int(people_flow_in_e),
                    'people_flow_out_e': int(people_flow_out_e),
                    'add_m': int(people_new_building * (nearest_station[-1 * n][-1] / dis)),
                    'add_e': int(people_new_building * (nearest_station[-1 * n][-1] / dis)),
                    'lng': row[1],
                    'lst': row[2]
                })

    return flow_metro


def find_nearest_station(my_location, metro_data):
    nearest_station = []

    for metro in metro_data:
        station_location = (metro[1], metro[2])
        distance = geodesic(my_location, station_location).kilometers
        if distance < 1.2:
            metro.append(distance)
            nearest_station.append(metro)

    return nearest_station


def get_nearby_roads_capacity(my_location, coord_centre, people, radius=750):

    latitude = my_location[0]
    longitude = my_location[1]
    # Получаем граф дорог вокруг заданных координат
    G = ox.graph_from_point((latitude, longitude), dist=radius, network_type='drive')

    # Получаем информацию о дорогах
    roads = ox.graph_to_gdfs(G, nodes=False, edges=True)

    # Извлекаем пропускную способность и другую информацию
    road_capacities = []
    for _, row in roads.iterrows():
        road_type = row.get('highway', 500)
        capacity = road_capacity.get(road_type, 500)
        name = row.get('name', 'Unnamed')  # Имя дороги

        # Извлекаем координаты дороги
        geometry = row.geometry
        coords = list(geometry.coords) if geometry is not None else []

        distance = geodesic(coord_centre, coords[len(coords) // 2]).kilometers

        if distance < 2.5:
            road_capacities.append({
                'name': name,
                'type': road_type,
                'capacity_m': (int(capacity * 0.65) + int(people * 0.3 / 1.2)),
                'capacity_e': (int(capacity * 0.89) + int(people * 0.3 / 1.2)),
                'add_m': int(people * 0.3 / 1.2 * 0.65),
                'add_e': int(people * 0.3 / 1.2 * 0.89),
                'length': row['length'],
                'coordinates': coords,
                'point': ((int(capacity * 0.65) + int(people * 0.3 / 1.2)) + (int(capacity * 0.89) + int(people * 0.3 / 1.2))) / (capacity * 2)
            })
        elif distance < 6:
            road_capacities.append({
                'name': name,
                'type': road_type,
                'capacity_m': (int(capacity * 0.52) + int(people * 0.3 / 1.2)),
                'capacity_e': (int(capacity * 0.8) + int(people * 0.3 / 1.2)),
                'add_m': int(people * 0.3 / 1.2 * 0.52),
                'add_e': int(people * 0.3 / 1.2 * 0.8),
                'length': row['length'],
                'coordinates': coords,
                'point': ((int(capacity * 0.52) + int(people * 0.3 / 1.2)) + (int(capacity * 0.8) + int(people * 0.3 / 1.2))) / (capacity * 2)
            })
        else:
            road_capacities.append({
                'name': name,
                'type': road_type,
                'capacity_m': (int(capacity * 0.6) + int(people * 0.3 / 1.2)),
                'capacity_e': (int(capacity * 0.7) + int(people * 0.3 / 1.2)),
                'add_m': int(people * 0.3 / 1.2 * 0.6),
                'add_e': int(people * 0.3 / 1.2 * 0.7),
                'length': row['length'],
                'coordinates': coords,
                'point': ((int(capacity * 0.6) + int(people * 0.3 / 1.2)) + (int(capacity * 0.7) + int(people * 0.3 / 1.2))) / (capacity * 2)
            })

    # Возвращаем результат в формате JSON
    return road_capacities
