import requests

# URL Overpass API
OVERPASS_URL = "http://overpass-api.de/api/interpreter"

# Запрос для получения дорог в Москве
overpass_query = """
[out:xml][timeout:600];
area["name"="Moscow"]["boundary"="administrative"]["admin_level"=4];
(
  way["highway"](area);
);
out body;
>;
out skel qt;
"""

response = requests.post(OVERPASS_URL, data={'data': overpass_query})

if response.status_code == 200:
    with open('moscow_roads.osm', 'wb') as f:
        f.write(response.content)
    print("Данные успешно загружены и сохранены в 'moscow_roads.osm'.")
else:
    print(f"Ошибка загрузки данных: {response.status_code}")


import osmium
import psycopg2
from shapely.geometry import LineString
import json

# Параметры подключения к базе данных
DB_PARAMS = {
    'dbname': 'moscow_roads',
    'user': 'moscow_user',
    'password': 'securepassword',
    'host': 'localhost',
    'port': '5432'
}

# Обработчик OSM данных
class RoadHandler(osmium.SimpleHandler):
    def __init__(self):
        super(RoadHandler, self).__init__()
        self.roads = []

    def way(self, w):
        if 'highway' in w.tags:
            highway = w.tags['highway']
            name = w.tags.get('name', 'unnamed')
            geometry = []
            for node in w.nodes:
                geometry.append((node.lon, node.lat))
            if len(geometry) >= 2:
                line = LineString(geometry)
                self.roads.append({
                    'osm_id': w.id,
                    'highway': highway,
                    'name': name,
                    'geom': json.dumps(line.__geo_interface__)
                })

# Функция для подключения к базе данных
def connect_db():
    conn = psycopg2.connect(**DB_PARAMS)
    return conn

# Функция для создания таблицы
def create_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS roads (
                id BIGSERIAL PRIMARY KEY,
                osm_id BIGINT UNIQUE,
                highway VARCHAR(50),
                name VARCHAR(255),
                geom GEOMETRY(LineString, 4326)
            );
        """)
        conn.commit()

# Функция для вставки данных
def insert_roads(conn, roads):
    with conn.cursor() as cur:
        for road in roads:
            try:
                cur.execute("""
                    INSERT INTO roads (osm_id, highway, name, geom)
                    VALUES (%s, %s, %s, ST_GeomFromGeoJSON(%s))
                    ON CONFLICT (osm_id) DO NOTHING;
                """, (road['osm_id'], road['highway'], road['name'], road['geom']))
            except Exception as e:
                print(f"Ошибка вставки OSM ID {road['osm_id']}: {e}")
        conn.commit()

def main():
    handler = RoadHandler()
    print("Парсинг OSM данных...")
    handler.apply_file('moscow_roads.osm')
    print(f"Найдено дорог: {len(handler.roads)}")

    print("Подключение к базе данных...")
    conn = connect_db()

    print("Создание таблицы (если необходимо)...")
    create_table(conn)

    print("Вставка данных в базу...")
    insert_roads(conn, handler.roads)
    print("Данные успешно импортированы.")

    conn.close()

if __name__ == "__main__":
    main()