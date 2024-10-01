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

    for row in nearest_station:
        for flow in data_metro_flow:
            if row[0] == flow[0] and row[3][0] == flow[3][0]:
                coord_metro = row[1], row[2]
                distance = geodesic(coord_centre, coord_metro).kilometers
                if distance < 5:
                    people_flow_out_m = 0.7 * 0.5 * ((0.5 * flow[2]) + people_new_building)
                    people_flow_in_m = 0.7 * 0.5 * ((0.5 * flow[1]) + people_new_building)

                    people_flow_out_e = 0.7 * 0.5 * ((0.5 * flow[2]) + people_new_building)
                    people_flow_in_e = 0.7 * 0.5 * ((0.5 * flow[1]) + people_new_building)
                else:
                    people_flow_out_m = 0.7 * 0.2 * ((0.5 * flow[2]) + people_new_building)
                    people_flow_in_m= 0.7 * 0.8 * ((0.5 * flow[1]) + people_new_building)
                    people_flow_out_e = 0.7 * 0.8 * ((0.5 * flow[2]) + people_new_building)
                    people_flow_in_e = 0.7 * 0.2 * ((0.5 * flow[1]) + people_new_building)

        flow_metro.append({
            'name': row[0],
            'Line': row[3],
            'people_flow_in_m': int(people_flow_in_m),
            'people_flow_out_m': int(people_flow_out_m),
            'people_flow_in_e': int(people_flow_in_e),
            'people_flow_out_e': int(people_flow_out_e),
            'lng': row[1],
            'lst': row[2]
        })

    return flow_metro


def find_nearest_station(my_location, metro_data):
    nearest_station = []

    for metro in metro_data:
        station_location = (metro[1], metro[2])
        distance = geodesic(my_location, station_location).kilometers
        if distance < 1.5:
            nearest_station.append(metro)

    return nearest_station


def get_nearby_roads_capacity(my_location, coord_centre, people, radius=500):

    latitude = my_location[0]
    longitude = my_location[1]
    # Получаем граф дорог вокруг заданных координат
    G = ox.graph_from_point((latitude, longitude), dist=radius, network_type='drive')

    # Получаем информацию о дорогах
    roads = ox.graph_to_gdfs(G, nodes=False, edges=True)

    # Извлекаем пропускную способность и другую информацию
    road_capacities = []
    for _, row in roads.iterrows():
        # Получаем тип дороги
        road_type = row.get('highway', 500)
        # Получаем пропускную способность из словаря или устанавливаем значение по умолчанию
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
                'capacity_m': (int(capacity * 0.4) + int(people * 0.3 / 1.2)),
                'capacity_e': (int(capacity * 0.9) + int(people * 0.3 / 1.2)),
                'length': row['length'],
                'coordinates': coords
            })
        elif distance < 6:
            road_capacities.append({
                'name': name,
                'type': road_type,
                'capacity_m': (int(capacity * 0.5) + int(people * 0.3 / 1.2)),
                'capacity_e': (int(capacity * 0.9) + int(people * 0.3 / 1.2)),
                'length': row['length'],
                'coordinates': coords
            })
        else:
            road_capacities.append({
                'name': name,
                'type': road_type,
                'capacity_m': (int(capacity * 0.75) + int(people * 0.3 / 1.2)),
                'capacity_e': (int(capacity * 0.75) + int(people * 0.3 / 1.2)),
                'length': row['length'],
                'coordinates': coords
            })

    # Возвращаем результат в формате JSON
    return road_capacities
