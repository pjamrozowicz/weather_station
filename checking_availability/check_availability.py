import urllib.request
import smtplib

#Web Server Address
address = 'http://example.net'

#SMTP AUTHENTICATION
username = 'username'
password = 'password'
MSG = """Subject: Problem With Establishing WebServer Availability
Check what went wrong!

Error Information:
%s"""


def send_allert(msg, error):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(username, password)
    server.sendmail(username, username, msg % error)
    server.quit()


if __name__ == '__main__':
    try:
        url = urllib.request.urlopen(address + "/availability/")
        response = url.read().decode('utf-8')
        if response != "STATUS: Available": raise Exception('Unrecognized Response From Webserver: %s' % response)
    except Exception as e:
        send_allert(MSG, e)

