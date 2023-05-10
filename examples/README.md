# README.md (rev.20230510)

The scripts are written for a single Raspberry Pi with 3 sensors, only because that's what I have here, but it's easy enough to adjust to your specific configuration.<br>
<br>
Samples are provided for easier editing, but see below to understand the steps involved.<br>
<br>
<p>
 HOW TO ADD MORE SENSORS<br>
 <br>
 Edit the "logtemp.sh" script in "/opt/rpi-ds18b20":
 
 Copy line 11:<br>
 <code>SENS3="28-051701be51ff" # Sensor 3 (change according to your sensor unique ID)</code><br> 
 and paste below as many copies as needed, then change the number, e.g. to add sensors #4 and #5:
 <pre>
 SENS4="28-0544444444ff" # Sensor 4 (change according to your sensor unique ID) 
 SENS5="28-0555555555ff" # Sensor 5 (change according to your sensor unique ID)</pre> 
  <br> 
 Copy line 31:<br>
 <code>TMP3=`cat $SENS3/temperature` # sensor 3</code><br>
 and paste below as many copies as needed, then change the numbers, e.g.
 <pre>
 TMP4=`cat $SENS4/temperature` # sensor 4 
 TMP5=`cat $SENS5/temperature` # sensor 5</pre>
 <br>
 Copy lines 39 and 40 together:<br>
 <pre>
 if ((TMP3==85000 || TMP3==nul)); then reset_sensor $SENS3 $TMP3; TMP3=`cat $SENS3/temperature`;
 if ((TMP3==85000 || TMP3==nul)); then TMP3='-'; fi; fi</pre>
 and paste below as many copies as needed, then change the numbers, e.g.
 <pre>
 if ((TMP4==85000 || TMP4==nul)); then reset_sensor $SENS4 $TMP4; TMP4=`cat $SENS4/temperature`; 
 if ((TMP4==85000 || TMP4==nul)); then TMP4='-'; fi; fi 
 if ((TMP5==85000 || TMP5==nul)); then reset_sensor $SENS5 $TMP5; TMP5=`cat $SENS5/temperature`; 
 if ((TMP5==85000 || TMP5==nul)); then TMP5='-'; fi; fi</pre>
 <br>
 Finally, add the sensors after $TMP3 on line 43:<br>
 <code>DATA=`date +"%F %X $TCPU $TMP1 $TMP2 $TMP3"`  # format log line</code><br>
 extending it to:<br>
 <code>DATA=`date +"%F %X $TCPU $TMP1 $TMP2 $TMP3 $TMP4 $TMP5"`  # format log line</code><br>
 </p>
 <br>
 <p>
 Likewise, edit the "showtemp.cgi" script in "/var/www/html/t":
 
 Copy line 15:<br>
 <code>$name3   = "Sensor 3"; # display name of sensor 3</code><br> 
 and paste below as many copies as needed, then change the numbers and optionally give it a more descriptive name, e.g. 
 <pre>
 $name4   = "Kitchen";  # display name of sensor 4
 $name5   = "Bedroom";  # display name of sensor 5</pre>
 <br>
 Add the sensors after $tempmc3 on line 33:<br>
 <code>($date,$time,$tempmc0,$tmpmc1,$tempmc2,$tempmc3) = split(" ",$line); # split array to read each value</code><br>
 extending it to:<br>
 <code>($date,$time,$tempmc0,$tmpmc1,$tempmc2,$tempmc3,tempmc4,tempmc5) = split(" ",$line); # split array to read each value</code><br>
 <br>
 Copy line 39:<br>
 <code>if ($tempmc3 ne "-") { $tempc3 = int($tempmc3/100)/10; } else { tempc3 = ''; }</code><br>
 and paste below as many copies as needed, then change the numbers, e.g.
 <pre>
 if ($tempmc4 ne "-") { $tempc4 = int($tempmc4/100)/10; } else { tempc4 = ''; }
 if ($tempmc5 ne "-") { $tempc5 = int($tempmc5/100)/10; } else { tempc5 = ''; }</pre>
 <br>
 Repeat the process for duplicating lines...<br>
 44: <code>$y3 .= "$tempc3,";</code><br>
 to: <code>$y4 .= "$tempc4,";</code><br>
 <br>
 51: <code>$tempf3 = int(1.8*$tempmc3/100)/10+32;</code><br>
 to: <code>$tempf4 = int(1.8*$tempmc4/100)/10+32;</code><br>
 <br>
 57: <code>$header .= " - $name3: " . ($tempmc3 ne "-") ? "$tempc3$degC / $tempf3$degF" : "---";</code><br>
 to: <code>$header .= " - $name4: " . ($tempmc4 ne "-") ? "$tempc4$degC / $tempf4$degF" : "---";</code><br>
 <br>
 78: <code>,{ label: "$name3", data: [$y3], borderColor: "teal",   fill: false }</code><br>
 to: <code>,{ label: "$name4", data: [$y4], borderColor: "blue",   fill: false }</code><br>
</p>
<br>
<p>
 HOW TO REMOVE A SENSOR<br>
 <br>
 Follow the same steps as above, but remove the entries with number 3 instead of copying/pasting new ones.<br>
 To only keep one DS18B20 sensor, also remove the entries with number 2, thus only keeping TMP1, $y1, $name1, etc.<br>
 <br>
 HOW TO LOG MULTIPLE RPIs TO THE SAME SERVER<br>
 <br>
 Each RPi should have its own cron job and "logtemp.sh" script, but each script should point to a different copy of "logtemp.cgi" on the server.<br>
 - For example, on the second RPi, in "logtemp.sh", change the URL variable to point to "http://your-server/t/logtemp2.cgi".<br>
 - On the server copy "logtemp.cgi" to "logtemp2.cgi" and edit it to change the "$logfile" variable to "temp2.log".<br>
 - Copy "showtemp.cgi" to showtemp2.cgi" and also edit the "$logfile" variable to "temp2.log".<br>
 - The same steps can be repeated for additional RPis.<br>
 - Each chart can then be viewed on its own page by calling the respective showtemp*.cgi from a browser.<br>
   It's also possible to display all the charts on the same page, but it's more complicated.<br>
   I can add an example for that if there is any demand for it.
