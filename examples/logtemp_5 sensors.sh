#!/bin/bash
# Template for 5 sensors
# Read, log and send temperature readings from CPU and external temperature sensors
# rev.20230510

LOGPATH="/opt/rpi-ds18b20" # location for log files (must be absolute path)
ERRLOG="temp_err.log"      # error log filename
TMPLOG="temp.log"          # temperatures log filename
URL="http://192.168.1.7/t/logtemp.cgi" # URL to server-side script (change according to your server address)
SENS1="28-041702432aff" # Sensor 1 (change according to your sensor unique ID)
SENS2="28-0417028cc1ff" # Sensor 2 (change according to your sensor unique ID)
SENS3="28-051701be51ff" # Sensor 3 (change according to your sensor unique ID)
SENS4="28-0544444444ff" # Sensor 4 (change according to your sensor unique ID)
SENS5="28-0555555555ff" # Sensor 5 (change according to your sensor unique ID)

# go to onewire device directory
pushd /sys/devices/w1_bus_master1 

#function to reset stuck sensor
reset_sensor () {
 echo 1 >w1_master_timeout;  # reduce bus scan time to 1 second
 echo >w1_master_remove $1;  # removed sensors are automatically rescanned
 sleep 2;                    # allow some time for the scan to occur
 echo 10 >w1_master_timeout; # revert bus scan delay to default
 echo 10 >$1/resolution;     # reduce resolution as we only need xx.x precision
 echo 1 >$1/features;        # enable sensor reading validity check
 date +"%F %X $1 $2" >>$LOGPATH/$ERRLOG # log reset details for further analysis
}

# read all temp sensors
TCPU=`cat /sys/class/thermal/thermal_zone0/temp` # CPU temperature
TMP1=`cat $SENS1/temperature` # sensor 1
TMP2=`cat $SENS2/temperature` # sensor 2
TMP3=`cat $SENS3/temperature` # sensor 3
TMP4=`cat $SENS4/temperature` # sensor 4
TMP5=`cat $SENS5/temperature` # sensor 5

#check sensor values, if invalid, reset and retry once
# 85000 = sensor initialized but not queried yet, nul = read error
if ((TMP1==85000 || TMP1==nul)); then reset_sensor $SENS1 $TMP1; TMP1=`cat $SENS1/temperature`;
if ((TMP1==85000 || TMP1==nul)); then TMP1='-'; fi; fi
if ((TMP2==85000 || TMP2==nul)); then reset_sensor $SENS2 $TMP2; TMP2=`cat $SENS2/temperature`;
if ((TMP2==85000 || TMP2==nul)); then TMP2='-'; fi; fi
if ((TMP3==85000 || TMP3==nul)); then reset_sensor $SENS3 $TMP3; TMP3=`cat $SENS3/temperature`;
if ((TMP3==85000 || TMP3==nul)); then TMP3='-'; fi; fi
if ((TMP4==85000 || TMP4==nul)); then reset_sensor $SENS4 $TMP3; TMP4=`cat $SENS4/temperature`;
if ((TMP4==85000 || TMP4==nul)); then TMP4='-'; fi; fi
if ((TMP5==85000 || TMP5==nul)); then reset_sensor $SENS5 $TMP3; TMP5=`cat $SENS5/temperature`;
if ((TMP5==85000 || TMP5==nul)); then TMP5='-'; fi; fi

# log sensor data locally and send remotely
DATA=`date +"%F %X $TCPU $TMP1 $TMP2 $TMP3 $TMP4 $TMP5"`  # format log line
echo $DATA >>$LOGPATH/$TMPLOG                             # write to log file
RES=`curl -s --data-urlencode "t=$DATA" $URL`             # send to server

popd # return shell to previous directory

exit 0
