# README.md (rev.20230509)

The scripts are written for a single Raspberry Pi with 3 sensors, only because that's what I have here, but it's easy enough to adjust to your specific configuration.
Samples are provided for easier editing, but see below to understand the steps involved.

HOW TO ADD MORE SENSORS
Edit the "logtemp.sh" script in "/opt/rpi-ds18b20".
Copy line 11:
 SENS3="28-051701be51ff" # Sensor 3 (change according to your sensor unique ID)
and paste below as many copies as needed, then change the number, e.g.
 SENS4="28-0544444444ff" # Sensor 4 (change according to your sensor unique ID)
 SENS5="28-0555555555ff" # Sensor 5 (change according to your sensor unique ID)

Copy line 31:
 TMP3=`cat $SENS3/temperature` # sensor 3
and paste below as many copies as needed, then change the numbers, e.g.
 TMP4=`cat $SENS4/temperature` # sensor 4
 TMP5=`cat $SENS5/temperature` # sensor 5

Copy lines 39 and 40 together:
 if ((TMP3==85000 || TMP3==nul)); then reset_sensor $SENS3 $TMP3; TMP3=`cat $SENS3/temperature`;
 if ((TMP3==85000 || TMP3==nul)); then TMP3='-'; fi; fi
and paste below as many copies as needed, then change the numbers, e.g.
 if ((TMP4==85000 || TMP4==nul)); then reset_sensor $SENS4 $TMP4; TMP4=`cat $SENS4/temperature`;
 if ((TMP4==85000 || TMP4==nul)); then TMP4='-'; fi; fi
 if ((TMP5==85000 || TMP5==nul)); then reset_sensor $SENS5 $TMP5; TMP5=`cat $SENS5/temperature`;
 if ((TMP5==85000 || TMP5==nul)); then TMP5='-'; fi; fi

Finally, add the sensors after $TMP3 on line 43:
 DATA=`date +"%F %X $TCPU $TMP1 $TMP2 $TMP3"`  # format log line
extending it to:
 DATA=`date +"%F %X $TCPU $TMP1 $TMP2 $TMP3 $TMP4 $TMP5"`  # format log line

Likewise, edit the "showtemp.cgi" script in "/var/www/html/t".
Copy line 15:
 $name3   = "Sensor 3"; # display name of sensor 3
and paste below as many copies as needed, then change the numbers and optionally give it a more descriptive name, e.g. 
 $name4   = "Kitchen";  # display name of sensor 4
 $name5   = "Bedroom";  # display name of sensor 5

Add the sensors after $tempmc3 on line 33:
 ($date,$time,$tempmc0,$tmpmc1,$tempmc2,$tempmc3) = split(" ",$line); # split array to read each value
extending it to:
 ($date,$time,$tempmc0,$tmpmc1,$tempmc2,$tempmc3,tempmc4,tempmc5) = split(" ",$line); # split array to read each value

Copy line 39:
 if ($tempmc3 ne "-") { $tempc3 = int($tempmc3/100)/10; } else { tempc3 = ''; }
and paste below as many copies as needed, then change the numbers, e.g.
 if ($tempmc4 ne "-") { $tempc4 = int($tempmc4/100)/10; } else { tempc4 = ''; }
 if ($tempmc5 ne "-") { $tempc5 = int($tempmc5/100)/10; } else { tempc5 = ''; }

Repeat the process for duplicating
 line 44: $y3 .= "$tempc3,";
      to: $y4 .= "$tempc4,";
 line 51: $tempf3 = int(1.8*$tempmc3/100)/10+32;
      to: $tempf4 = int(1.8*$tempmc4/100)/10+32;
 line 57: $header .= " - $name3: " . ($tempmc3 ne "-") ? "$tempc3$degC / $tempf3$degF" : "---";
      to: $header .= " - $name4: " . ($tempmc4 ne "-") ? "$tempc4$degC / $tempf4$degF" : "---";
 line 78: ,{ label: "$name3", data: [$y3], borderColor: "teal",   fill: false }
      to: ,{ label: "$name4", data: [$y4], borderColor: "blue",   fill: false }

HOW TO REMOVE SENSORS
Follow the same steps as above, but remove the entries with number 3 instead of copying/pasting new ones.

HOW TO LOG MULTIPLE RPIs
Each RPi should have its own cron job and "logtemp.sh" script, but each script should point to a different copy of "logtemp.cgi" on the server.
For example, on the second RPi, in "logtemp.sh", change the URL variable to point to "http://your-server/t/logtemp2.cgi"
On the server copy "logtemp.cgi" to "logtemp2.cgi" and edit it to change the "$logfile" variable to "temp2.log".
Copy "showtemp.cgi" to showtemp2.cgi" and also edit the "$logfile" variable to "temp2.log"
The same steps can be repeated for additional RPis.
Each chart can then be viewed on its own page by calling the respective showtemp*.cgi from a browser.
It's also possible to display all the charts on the same page, but it's more complicated. I'LL add an example for that if there is any demand for it.
