import smtplib
import sqlite3
import datetime

database = "/home/weather_station/db.sqlite3"
fromaddr = 'weather.station.krk@gmail.com'

MSG = "Welcome !\n" \
      "Today average temperature was: %s\n" \
      "Maximum: %s\n" \
      "Minimum: %s\n"

#SMTP Authentication
username = 'your_username'
password = 'your_password'

#DATA SQL Queries
queries = {
    "max_temp": "SELECT max(temperature) FROM temperatures_temperature WHERE strftime('%Y-%m-%d',measured)=?",
    "min_temp": "SELECT min(temperature) FROM temperatures_temperature WHERE strftime('%Y-%m-%d',measured)=?",
    "avg_temp": "SELECT avg(temperature) FROM temperatures_temperature WHERE strftime('%Y-%m-%d',measured)=?"
}


def send_mails(data, addresses):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, addresses, MSG % (data['avg_temp'], data['max_temp'], data['min_temp']))
    server.quit()


def get_specific_temperature(query):
    today = str(datetime.date.today())
    return get_database_data(query, [today])[0][0]


def get_all_temperatures():
    temperatures = {}
    for tmp_type, query in queries.items():
        temperatures[tmp_type] = get_specific_temperature(query)
    return temperatures


def get_database_data(query, args=[]):
    connection = sqlite3.connect(database)
    with connection:
        cursor = connection.cursor()
        results = cursor.execute(query, args).fetchall()
    connection.close()
    return results


def get_receivers():
    query = "SELECT email FROM temperatures_newsletter"
    results = get_database_data(query)
    receivers = []
    for result in results:
        receivers.append(result[0])
    return receivers


def run():
    receivers = get_receivers()
    temperatures = get_all_temperatures()
    send_mails(temperatures, receivers)

run()