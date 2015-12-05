# Weather Station

## Description
Measure the temperature using your Raspberry device, it's really simple! All you need is a Raspberry, temperature sensor and our project.

  - Beautiful graphs
  - Exact sunrise and sunset time
  - 24 hours maximum and minimum temperature
  - Average day, month and year temperature

## Requirements
You will need 2 machines to run this project:
- [Raspberry Pi] Pre Installed Raspbery Pi with temperature sensor
- [WebServer] VPS or machine with Ubuntu 15.04 OS ( You can try to run WebServer directly on your Raspberry device but this way is not supported by this tutorial )
- Source files which you need to download: https://github.com/bumbur/weather_station/archive/master.zip

## Prerequisities
You will need to create an email that will be used to handle server exceptions and
send emails to people registered for your newsletter.

The easiest way is to create a brand new mail in Gmail and follow these instructions:
http://docs.helpscout.net/article/120-smtp-settings to make your account available for some scripts.

---

## Installation
### WebServer
If you would like to use ssh on Ubuntu 15.04 you need to login as root and type this in terminal: ```$ sudo apt-get install openssh-server ```
Additionally, you can also login via SSH as a root user but you need to change this line in /etc/ssh/sshd_config:
```PermitRootLogin without-password```
to
```PermitRootLogin yes```
and restart the SSH server: ```$ sudo service ssh restart ```

1. Make sure you have already installed Ubuntu 15.04 Server (Vivid Vervet)
2. **Log in to root user**
3. Download source mentioned above
4. There is Python 3.4.3 installed by default 
5. Change your timezone by typing in console: ```$ dpkg-reconfigure tzdata``` and check appropriate options
6. Restart your system
7. Place web_requirements.txt in, for example, **/root** location and go to this location
8. Install pip3 by typing in console ```$ sudo apt-get install python3-pip```
9. Install all necessary dependencies: ```$ pip3 install -r web_requirements.txt```
10. Place 'weather_station' folder in /home directory
11. Go to /home/weather_station/weather_station
12. Rename file **settings_secret.py.template** to **settings_secret.py**
13. Go here: http://www.miniwebtool.com/django-secret-key-generator/
14. Click "Generate Django Secret Key"
15. Copy Generated Django Secret Key
16. Open **settings_secret.py**
17. Paste generated value instead **your-secret-key** (between ' ')
18. Save **settings_secret.py**
19. **Extract** 'scripts' folder content in /root directory
20. Open send_mail.py file
21. In the SMTP section replace username and password with your gmail account username and password
22. Change variable **fromaddr** to your gmail email, for example: 'weather123@gmail.com'
23. Go to the /home/weather_station directory
24. Type this in command line: ```$ python3 manage.py makemigrations temperatures```
25. and ```$ python3 manage.py migrate```
26. Now open crontab: ```$ crontab -e```
27. Add this line at the end: **00 20 * * * python3 /root/send_mail.py**
28. Save crontab and leave it
29. You can now go to the /home/weather_station and run server: ```$ python3 manage.py runserver 0.0.0.0:80```

### Raspberry Pi 
1. Make sure that you have clean Raspbian OS installed
2. Install Python 3.5
3. Install all necessary dependencies: ```$ pip install rasp_requirements.txt```

This project was implemented by Przemysław Jamrozowicz and Piotr Jatkowski as a Python