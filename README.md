# rpi-ds18b20 rev.20230502
Log multiple ds18b20 onewire temperature sensors from RPi to a web server.

The goal of this project is to make it quick and easy to regularly log temperature sensors from a Raspberry Pi and send the readings to a web server, where the readings can be viewed on a line chart. The same RPi can also be the web server.

REQUIREMENTS
On the RPi side:
- OneWire must be enabled, typically in the /boot/config.txt file or by using the 'raspi-config' command.
  (see the section on gpio for more details)
- the cron service (or equivalent) must be running to regularly collect sensor data.
  (can be installed with "apt install cron" command)
- Curl (or wget, by adapting the script)
  (can be installed with "apt install curl" command)
On the web server side:
- Perl, which is usually installed by default (tested with Perl v5.20.2 but should work with older versions)
- Apache or any web server able to run CGI scripts (tested with Apache 2.4.10 raspbian)
  (can be installed with "apt install apache2" command)

HOW IT WORKS
On the RPi side:
The main shell script (logtemp.sh) is called regularly by a cron job and logs the temperature from multiple sensors, then sends the data to another server using Curl.

On the web server side:
Two perl scripts are used. One script (logtemp.cgi) receives the data and save it to a log whenever the RPi sends it.
The other (showtemp.cgi) processes the log and outputs a web page to display the data in a chart using javascript from Chart.js

DETAILS
By default the RPi script resides in /opt/ds18b20/logtemp.sh and the logs are saved to the same directory.
It reads the temperature from the CPU and 3 ds18b20 sensors, but the script can be easily changed to accomodate any number of sensors.
If a sensor returns and invalid value, the script will attempt to reset the sensor and retry reading the value once. It will also log the error to provide an easier way to analyze recurring sensor failures than scanning through the full log file.
If it fails on the second try, it will log "-" as the temperature for that sensor (so that the chart can skip the invalid data point without disturbing the display of valid ones).
Finally, the same temperature readings are sent to the web server, by calling its t.cgi script with the 4 temperature values as parameters.
The cron job can be run as frequently or rarely as desired, the default of every 10 minute seems like a good compromise because it provides enough datapoints for typically slow environmental changes, while growing the log file by less than 10KB per day.

By default the web server scripts reside in /var/www/html/t and the log is saved to the same directory. If the scripts are placed in a different directory, e.g. /var/www/cgi-bin, the URL should be adjusted accordingly in logtemp.sh on the RPi.

The log created on the web server is identical to the one on the RPi
