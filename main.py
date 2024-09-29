from geopy.distance import geodesic
import osmnx as ox
import geopandas as gpd
from shapely.geometry import Point
from input import *


def people_in_building(floors, square, type_building):
    people_new_building = -1

    if type_building == 'economy':
        people_new_building = floors * square / 25 * 0.57
    elif type_building == 'office':
        people_new_building = floors * square / 35 * 0.57
    elif type_building == 'comfort':
        people_new_building = floors * square / 45 * 0.57

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
                    people_flow_out_m = 0.5 * ((0.5 * flow[2]) + people_new_building)
                    people_flow_in_m = 0.5 * ((0.5 * flow[1]) + people_new_building)

                    people_flow_out_e = 0.5 * ((0.5 * flow[2]) + people_new_building)
                    people_flow_in_e = 0.5 * ((0.5 * flow[1]) + people_new_building)
                else:
                    people_flow_out_m = 0.2 * ((0.5 * flow[2]) + people_new_building)
                    people_flow_in_m= 0.8 * ((0.5 * flow[1]) + people_new_building)
                    people_flow_out_e = 0.8 * ((0.5 * flow[2]) + people_new_building)
                    people_flow_in_e = 0.2 * ((0.5 * flow[1]) + people_new_building)

        flow_metro.append([row[0], row[3], int(people_flow_in_m), int(people_flow_out_m), int(people_flow_in_e), int(people_flow_out_e), row[1], row[2]])

    return flow_metro


def find_nearest_station(my_location, metro_data):
    nearest_station = []

    for metro in metro_data:
        station_location = (metro[1], metro[2])
        distance = geodesic(my_location, station_location).kilometers
        if distance < 1.5:
            nearest_station.append(metro)

    return nearest_station


def find_nearest_roads(my_location):
    ox.config(use_cache=True, log_console=True)

    lat = my_location[0]
    lon = my_location[1]

    radius = 1000  # 1 км

    point = Point(lon, lat)

    gdf_point = gpd.GeoDataFrame([{'geometry': point}], crs="EPSG:4326")

    gdf_point = gdf_point.to_crs(epsg=3857)

    x, y = gdf_point.geometry.x.iloc[0], gdf_point.geometry.y.iloc[0]

    G = ox.graph_from_point((lat, lon), dist=radius, network_type='drive')

    edges = ox.graph_to_gdfs(G, nodes=False, edges=True)

    edges = edges.to_crs(epsg=3857)

    point_merc = Point(x, y)

    edges['distance'] = edges.geometry.apply(lambda geom: geom.distance(point_merc))

    geojson_data = edges.to_json()

    # Если нужно, можно загрузить обратно в Python как словарь
    nearest_roads = json.loads(geojson_data)

    return nearest_roads # TODO
