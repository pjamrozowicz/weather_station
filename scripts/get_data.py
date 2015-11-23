import sqlite3

database = "/home/weather_station/db.sqlite3"

connection = sqlite3.connect(database)
with connection:
    cursor = connection.cursor()
    query = 'SELECT * FROM temperatures_temperature'
    for row in cursor.execute(query):
        print(row)
connection.close()