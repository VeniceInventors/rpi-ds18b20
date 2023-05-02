# rpi-ds18b20 rev.20230502
Log multiple temperature RPi sensors to a chart server

The purpose of this code is to read temperature sensors reading from a Raspberry Pi and send the readings to a web server where the readings can be viewed on a line chart. If the RPi with the sensors is also running the web server, it only needs two scripts and one log file.

The main shell script (logtemp) is called regularly by a cron job and logs the temperature from multiple sensors, then sends the data to another server using Curl
On the server side two perl scripts are used, one to receives the data and save it to a log, the other to display the data in a chart using chart,js

The cron job can be run as frequently or rarely as desired, I like to set it to a 10 minutes interval because it provides enough datapoints for relatively slow changes, while keeping the log file growing less than 10KB per day.

