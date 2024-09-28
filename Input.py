from lyb import *


db_config = {
    'dbname': 'qablit79',
    'user': 'qablit79_user',
    'password': 'kPp7GjQFEJLEff1qPXuwOp4BwKPzkUmu',
    'host': 'dpg-crg5qcjv2p9s73a8f8vg-a.oregon-postgres.render.com',
    'port': '5432'
}


with open('data-62743-2024-09-03.json', 'r', encoding='cp1251') as file:
    data = json.load(file)


data_metro_flow = []

for row in data:
    if row['Year'] == 2024 and row['Quarter'] == 'I квартал':
        data_metro_flow.append([row['NameOfStation'], int(row['IncomingPassengers'] / 91), int(row['OutgoingPassengers'] / 91), row['Line']])


types_building = ['economy', 'comfort', 'office']
my_location = (55.680458, 37.674418)
coord_centre = 55.752507, 37.623150

test_floors = 9
test_square = 1000
test_type_building = 'economy'

cursor = None
connection = None

try:
    connection = psycopg2.connect(**db_config)

    cursor = connection.cursor()

    query = """
     SELECT name, latitude, longitude, name_line
     FROM metro;
        """

    cursor.execute(query)

    stations = cursor.fetchall()

    metro_data = []

    for station in stations:
        station_name = station[0][0]
        latitude = station[1]
        longitude = station[2]
        line_name = station[3][0]
        metro_data.append([station_name, latitude, longitude, line_name])


except Exception as error:
    print(f"Ошибка при работе с базой данных: {error}")

finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()
