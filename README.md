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

## Installation
### WebServer
1. Make sure you have already installed clean Ubuntu 15.04 Server (Vivid Vervet)
2. There is Python 3.4.3 installed by default 
3. **Log in to root user**
4. Change your timezone by typing in console: ```$ dpkg-reconfigure tzdata``` and check appropriate options
5. Restart your system
6. Install pip3 by typing in console ```$ sudo apt-get install python3-pip```
7. Install all necessary dependencies: ```$ pip3 install -r web_requirements.txt```
8. Place 'weather_station' folder in /home directory
9. Go to /home/weather_station/weather_station
10. Rename file **settings_secret.py.template** to **settings_secret.py**
11. Go here: http://www.miniwebtool.com/django-secret-key-generator/
12. Click "Generate Django Secret Key"
13. Copy Generated Django Secret Key
14. Open **settings_secret.py**
15. Paste generated value instead **your-secret-key** (between ' ')
16. Save **settings_secret.py**
17. **Extract** 'scripts' folder content in /root directory
18. Go to the /home/weather_station directory
19. Type this in command line: ```$ python3 manage.py makemigrations temperatures```
20. and ```$ python3 manage.py migrate```
21. Now open crontab: ```$ crontab -e```
22. Add this line at the end: **00 20 * * * python3 /root/send_mail.py**
23. Save crontab and leave it
24. You can now go to the /home/weather_station and run server: ```$ python3 manage.py runserver 0.0.0.0:80```

### Raspberry Pi 
1. Make sure that you have clean Raspbian OS installed
2. Install Python 3.5
3. Install all necessary dependencies: ```$ pip install rasp_requirements.txt```
4. 

This project was implemented by Przemys³aw Jamrozowicz and Piotr Jatkowski as a Python classes assignment. The idea belongs to our teacher dr Leszek Grzanka.