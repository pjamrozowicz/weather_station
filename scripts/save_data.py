import sqlite3
import sys
import datetime

database = "/home/weather_station/db.sqlite3"


def parse_data():
    sys.argv.pop(0)
    try:
        measured_time = sys.argv[3] + " " + sys.argv[4]
        measured_time = datetime.datetime.strptime(measured_time, "%Y-%m-%d %H:%M:%S")
        correctness = sys.argv[1] == 'True'
        data = [float(sys.argv[0]), correctness, str(sys.argv[2]), measured_time]
    except: wrong_arguments_passed()
    return tuple(data)

def wrong_arguments_passed():
    print("Wrong arguments passed!")
    sys.exit(-1)


def save_data_to_database(data):
    connection = sqlite3.connect(database)
    with connection:
        cursor = connection.cursor()
        query = 'INSERT INTO temperatures_temperature (temperature, correctness, description, measured) VALUES (?, ?, ?, ?)'
        cursor.execute(query, data)
        connection.commit()
    connection.close()

if len(sys.argv) < 6:
    wrong_arguments_passed()

data = parse_data()
save_data_to_database(data)