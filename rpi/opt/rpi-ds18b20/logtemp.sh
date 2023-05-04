#!/bin/bash
# Read, log and send temperature readings from CPU and external temperature sensors (rev.20230504)

DIR="/opt/rpi-ds18b20" # location for log files (must be absolute path)
ERRLOG="temp_err.log" # error log filename
TMPLOG="temp.log" # temperatures log filename
URL="http://192.168.1.7/t/logtemp.cgi" # URL to server-side script (change according to your server address)
SENS1="28-041702432aff" # change according to your sensor unique ID
SENS2="28-0417028cc1ff" # change according to your sensor unique ID
SENS3="28-051701be51ff" # change according to your sensor unique ID

# go to onewire device directory
pushd /sys/devices/w1_bus_master1 

#function to reset stuck sensor
reset_sensor () {
 echo >w1_master_remove $1; # removed sensors are automatically rescanned
 sleep 6; # allow some time for the scan to occur
 echo 10 >$1/resolution; # reduce resolution as we only need xx.x precision
 echo 1 >$1/features; # enable sensor reading validity check
 date +"%F %X $1" >>$DIR/$ERRLOG # log resets to make it easier to analyze recurring issues
}

# read all temp sensors
TCPU=`cat /sys/class/thermal/thermal_zone0/temp` # CPU temperature
TMP1=`cat $SENS1/temperature` # sensor 1
TMP2=`cat $SENS2/temperature` # sensor 2
TMP3=`cat $SENS3/temperature` # sensor 3

#check sensor values, if invalid, reset and retry once
# 85000 = sensor initialized but not queried yet, nul = read error
if ((TMP1==85000 || TMP1==nul)); then reset_sensor $SENS1; TMP1=`cat $SENS1/temperature`;
if ((TMP1==85000 || TMP1==nul)); then TMP1='-'; fi; fi
if ((TMP2==85000 || TMP2==nul)); then reset_sensor $SENS2; TMP2=`cat $SENS2/temperature`;
if ((TMP2==85000 || TMP2==nul)); then TMP2='-'; fi; fi
if ((TMP3==85000 || TMP3==nul)); then reset_sensor $SENS3; TMP3=`cat $SENS3/temperature`;
if ((TMP3==85000 || TMP3==nul)); then TMP3='-'; fi; fi

# log sensor data locally and send remotely
DATA=`date +"%F %X $TCPU $TMP1 $TMP2 $TMP3"`
echo $DATA >>$DIR/$TMPLOG
RES=`curl -s --data-urlencode "t=$DATA" $URL`

popd # return shell to previous directory

exit 0
