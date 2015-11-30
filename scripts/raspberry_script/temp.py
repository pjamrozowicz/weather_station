import paramiko
import socket
import datetime
import sqlite3
import smtplib

"""
Configuration Options
"""
SENSOR_ID = '28-000006ca986b'
SENSOR_FILE = '/sys/bus/w1/devices/' + SENSOR_ID + '/w1_slave'
ERROR_MSG = 'ERROR'
SUCCESS_MSG = 'SUCCESS'
REMOTE_CONNECTION = True
LOCAL_DATABASE = 'PATH_TO_DB'

"""
SSH Authentication
"""
hostname = 'hostname'
username = 'username'
password = 'password'

"""
Email Authentication
"""
username = 'your_login'
password = 'your_password'

"""
Server Messages
"""

TEMPERATUE_MEASURE_FAILURE = """Subject: TEMPERATURE MEASURE FAILURE
Couldn't obtain the current temperature.
Error Status:
%s
"""

VPS_LOGIN_FAILURE = """Subject: VPS LOGIN FAILURE
Couldn't connect to VPS
Error Status:
%s"""

EXECUTE_COMMAND_FAILURE = """Subject: EXECUTE COMMAND FAILURE
Couldn't execute Python command
Error Status:
%s"""


def send_mail(msg):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(username,password)
    server.sendmail(username, username, msg)
    server.quit()


def remote_saving_script(result):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh_client.connect(hostname, username=username, password=password)
        command = 'python save_data.py %s %s %s %s' % (result[0], result[1], result[2], result[3])
        ssh_client.exec_command(command)
    except (paramiko.BadHostKeyException, paramiko.AuthenticationException, paramiko.SSHException, socket.error) as e:
        send_mail(VPS_LOGIN_FAILURE % e)
    except paramiko.SSHException as e:
        send_mail(EXECUTE_COMMAND_FAILURE % e)


def local_saving_script(result):
    connection = sqlite3.connect(LOCAL_DATABASE)
    with connection:
        cursor = connection.cursor()
        query = "INSERT INTO temperatures_temperature (temperature, correctness, description, measured) VALUES (?, ?, ?, ?)"
        cursor.execute(query, tuple(result))
        connection.commit()
    connection.close()


def run_saving_script(result):
    if not result[1]:
        send_mail(TEMPERATUE_MEASURE_FAILURE % result[2])
    else:
        if REMOTE_CONNECTION:
            remote_saving_script(result)
        else:
            local_saving_script(result)


def prepare_result(temperature):
    measured = datetime.datetime.now().replace(microsecond=0)
    if temperature == ERROR_MSG:
        result = [0.0, False, ERROR_MSG, measured]
    else:
        result = [temperature, True, SUCCESS_MSG, measured]
    return result


def read_temperature():
    """ Get a temperature from file.
    If cannot open file or find temperature then
    returning ERROR_MSG else temperature as float number
    """
    try:
        t = open(SENSOR_FILE, mode='r')
        line = t.readlines()[1]
    except IOError:
        data = ERROR_MSG
    else:
        t.close()

    if 'data' not in locals():
        index = line.find("t=")+2
        if index == -1:
            data = ERROR_MSG
        else:
            data = float(line[index:])/1000.0
    return data

result = prepare_result(read_temperature())
run_saving_script(result)
