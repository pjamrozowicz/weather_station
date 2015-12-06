# Weather Station

## Description
Measure the temperature using your Raspberry device, it's really simple! All you need is a Raspberry, temperature sensor and our project.

  - Beautiful graphs
  - Exact sunrise and sunset time
  - 24 hours maximum and minimum temperature
  - Average day, month and year temperature

## Requirements
- Raspbery Pi 
- Temperature sensor DS18B20
- (Optional) VPS with Ubuntu 15.04 OS - if you want to make your website available on the Internet
- Source files: https://github.com/bumbur/weather_station/archive/master.zip
- Gmail account

## Prerequisities
You will need to create an email that will be used to handle server exceptions and
send emails to people registered for your newsletter.

The easiest way is to create a brand new Gmail account and follow these instructions: http://docs.helpscout.net/article/120-smtp-settings to make your account available for some scripts.

---

## Installation
### Raspberry
This tutorial covers installation on Raspberry Model B Revision 2.0 with temperature sensor DS18B20. Firstly, connect temperature sensor to the Raspberry and then install Raspbian Jessie Lite on your Raspberry.

Connect to Raspberry and add the following line to /boot/config.txt: 
>dtoverlay=w1-gpio

Reboot with:
```sh
$ sudo reboot
```
Run commands:
```sh
$ sudo modprobe w1-gpio
$ sudo modprobe w1-therm
$ sudo dpkg-reconfigure tzdata
$ sudo apt-get install python3
$ sudo apt-get install python3-pip
```

Go to home directory and run:
```sh
$ sudo wget https://github.com/bumbur/weather_station/archive/master.zip
$ sudo unzip master.zip
$ cd weather_station-master
$ sudo pip3 install -r rasp_requirements.txt
```
Move all scripts from 'scripts' folder to /root directory (use root user if necessary).


If you are planning to run your website on VPS server please skip these steps (until temp.py file part):
```sh
$ cd /home/weather_station-master/weather_station/weather_station
$ sudo mv settings_secret.py.template settings_secret.py
```
Go here: http://www.miniwebtool.com/django-secret-key-generator/, generate your key and paste it to settings_secret.py.

Then run:
```sh
cd /home
$ sudo mv weather_station-master/weather_station/ /home/weather_station
$ cd /home/weather_station
$ sudo python3 manage.py makemigrations temperatures
$ sudo python3 manage.py migrate
$ sudo python3 manage.py runserver 0.0.0.0:8000
```
Now you can access your website on any device in your local network by going to web browser and using IP address of your Raspberry followed by port number. It will look like this: 192.168.X.XX:8000.
Stop the server for a while and continue with following steps (at the end run it again with the same command).

Open /home/weather_station-master/raspberry_scripts/temp.py file and enter your Gmail account credentials. You can also enter SSH authentication data for your VPS server if your are going to use one.
Set variable REMOTE_CONNECTION:
- True - if you are going to use VPS
- False - if you aren't going to use VPS


Open crobtab:
```sh
$ sudo crontab -e
```
Add following line:
```*/10 * * * * sudo python3 /home/weather_station-master/raspberry_scripts/temp.py```

Script will save temperature info to the database every 10 minutes.

Set up newsletter now. Open send_mail.py file from root directory. Change variable fromaddr to your Gmail address, for example: ‘weather123@gmail.com’, enter your username and password under SMTP section, save. Open crontab again and add the following line: 
```00 20 * * * python3 /root/send_mail.py```

If you are not using VPS run your server again but in the background this time so it won't stop when you leave terminal.
If you want to use VPS, please carry on with the instruction.

### WebServer on VPS
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

This project was implemented by Przemysław Jamrozowicz and Piotr Jatkowski as a Pytho class assignment.The idea belongs to our techer dr Leszek Grzanka.