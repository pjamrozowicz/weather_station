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
This tutorial covers installation on Raspberry Model B Revision 2.0 with temperature sensor DS18B20.

Connect temperature sensor to the Raspberry:
http://www.modmypi.com/blog/ds18b20-one-wire-digital-temperature-sensor-and-the-raspberry-pi
Install Raspbian Jessie Lite on your Raspberry:
- download: https://www.raspberrypi.org/downloads/raspbian/
- installation: http://www.raspberry-projects.com/pi/pi-operating-systems/win32diskimager

Turn on your Raspberry and plug it in to the router with Ethernet cable.

You have to find IP address of your Raspberry: https://www.raspberrypi.org/documentation/troubleshooting/hardware/networking/ip-address.md

Open any SSH client, for example Putty (http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html), enter IP address of your raspberry and hit connect.
Default login credentials are:
- login:pi
- password:raspberry

After logging in add the following line to /boot/config.txt: 
>dtoverlay=w1-gpio

Reboot with:
```sh
sudo reboot
```

Download script named "raspberry-install" from this repository and save it on your raspberry with the same name (you can just copy-paste it).
Make sure it has all the necessary rights (to be sure, you can run command: sudo chmod 777 raspberry-install).
Run:
- if you are not going to use VPS:
```sh
sudo ./raspberry-install local
```
Go here: http://www.miniwebtool.com/django-secret-key-generator/, generate your key and paste it to settings_secret.py which is inside home\weather_station\weather_station directory.

```sh
		sudo screen
		cd /home/weather_station
		sudo python3 manage.py runserver 0.0.0.0:8000
		sudo screen -d
```

Now you can access your website on any device in your local network by going to web browser and using IP address of your Raspberry followed by port number. It will look like this: 192.168.X.XX:8000.

- if you are going to use VPS:
```sh
sudo ./raspberry-install
```

Continue in any case:

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
```00 20 * * * python3 /home/send_mail.py```


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
19. **Extract** 'scripts' folder content in /home directory
20. Open send_mail.py file
21. In the SMTP section replace username and password with your gmail account username and password
22. Change variable **fromaddr** to your gmail email, for example: 'weather123@gmail.com'
23. Go to the /home/weather_station directory
24. Type this in command line: ```$ python3 manage.py makemigrations temperatures```
25. and ```$ python3 manage.py migrate```
26. Now open crontab: ```$ crontab -e```
27. Add this line at the end: **00 20 * * * python3 /home/send_mail.py**
28. Save crontab and leave it
29. You can now go to the /home/weather_station and run server: ```$ python3 manage.py runserver 0.0.0.0:80```

### Checking Availability
If you would like to simultanously check web server's availability you can use script from checking_availability folder (check_availability.py). It depends on you, where you want to host this script. What's more important, is fact that you need to replace following variables in this script file(check_availability.py):
* **address** variable should be set to your web server address, for example: 'http://example.net'
* **username** and **password** variables should be set according to your gmail account created before. The script will use this email to send you notifications about failures.

Now you can manually run this script whenever you want, add it to crontab (in the same way you've added other scripts in this tutorial). The choice is yours.

---

This project was implemented by Przemysław Jamrozowicz and Piotr Jatkowski as a Python class assignment.The idea belongs to our techer dr Leszek Grzanka.
