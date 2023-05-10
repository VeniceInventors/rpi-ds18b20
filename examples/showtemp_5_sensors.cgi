#! /usr/bin/perl
# template for 5 sensors
# showtemp.cgi - display chart from temp.log data (rev.20230510)
# from a web browser: "http://<your_server_address>/t/showtemp.cgi?days=1&hours=12"
# or to see last 24h: "http://<your_server_address>/t/showtemp.cgi"

print qq~Content-Type: text/html\n\n~; # this should be first or errors won't print in browser

### user-defined variables ###
$minutes = 10;         # minutes per log line (adjust according to RPi cron job)
$logfile = "temp.log"; # log filename (can use relative or absolute path)
$title   = "RPi-DS18B20 Temperature Chart"; # page title
$name0   = "CPU";      # display name of CPU temp
$name1   = "Sensor 1"; # display name of sensor 1
$name2   = "Sensor 2"; # display name of sensor 2
$name3   = "Sensor 3"; # display name of sensor 3
$name4   = "Sensor 4"; # display name of sensor 4
$name5   = "Sensor 5"; # display name of sensor 5
### end of user-defined variable ###

use CGI;      # provides access to GET/POST parameters from browser
$q = new CGI; # initialize CGI object

# by specifying days or hours, client can limit the chart size
$d = $q->param('days');  # get days value from query string
$h = $q->param('hours'); # get hours value from query string
if ($d) { $lines  = int((60/$minutes) * 60 * 24 * $d) }   # set number of lines per day to read from log
if ($h) { $lines += int((60/$minutes) * 60 * $h) }        # set number of lines per hours to read from log
unless ($lines) { $lines = int((60/$minutes) * 60 * 24) } # default to the last 24 hours if no value was provided

@log = `tail -n $lines $logfile`;       # retrieve desired number of lines from log
$degC = '\\u00B0C'; $degF = '\\u00B0F'; # shorthand for degrees symbol

# scan through each line of the log
foreach $line (@log) { chomp; # remove newline char
 ($date,$time,$tempmc0,$tmpmc1,$tempmc2,$tempmc3,$tempmc4,$tempmc5) = split(" ",$line); # split array to read each value
 $x .= '"' . substr($date,5,5) . " " . substr($time,0,5) . '",';      # shorten date/time to "MM-DD hh:mm"
 # format millicelsius values to xx.x, or leave empty if sensor reading was invalid
 if ($tempmc0 ne "-") { $tempc0 = int($tempmc0/100)/10; } else { tempc0 = ''; }
 if ($tempmc1 ne "-") { $tempc1 = int($tempmc1/100)/10; } else { tempc1 = ''; }
 if ($tempmc2 ne "-") { $tempc2 = int($tempmc2/100)/10; } else { tempc2 = ''; }
 if ($tempmc3 ne "-") { $tempc3 = int($tempmc3/100)/10; } else { tempc3 = ''; }
 if ($tempmc4 ne "-") { $tempc4 = int($tempmc4/100)/10; } else { tempc4 = ''; }
 if ($tempmc5 ne "-") { $tempc5 = int($tempmc5/100)/10; } else { tempc5 = ''; }
 # create arrays of values for chart
 $y0 .= "$tempc0,";
 $y1 .= "$tempc1,";
 $y2 .= "$tempc2,";
 $y3 .= "$tempc3,";
 $y4 .= "$tempc4,";
 $y5 .= "$tempc5,";
}

# convert most recent temp values from C to F, for chart title
$tempf0 = int(1.8*$tempmc0/100)/10+32;
$tempf1 = int(1.8*$tempmc1/100)/10+32;
$tempf2 = int(1.8*$tempmc2/100)/10+32;
$tempf3 = int(1.8*$tempmc3/100)/10+32;
$tempf4 = int(1.8*$tempmc4/100)/10+32;
$tempf5 = int(1.8*$tempmc5/100)/10+32;

# display name and C/F temps or "---" to emphasize invalid readings
$header  =    "$name0: " . ($tempmc0 ne "-") ? "$tempc0$degC / $tempf0$degF" : "---";
$header .= " - $name1: " . ($tempmc1 ne "-") ? "$tempc1$degC / $tempf1$degF" : "---";
$header .= " - $name2: " . ($tempmc2 ne "-") ? "$tempc2$degC / $tempf2$degF" : "---";
$header .= " - $name3: " . ($tempmc3 ne "-") ? "$tempc3$degC / $tempf3$degF" : "---";
$header .= " - $name4: " . ($tempmc4 ne "-") ? "$tempc4$degC / $tempf4$degF" : "---";
$header .= " - $name3: " . ($tempmc5 ne "-") ? "$tempc5$degC / $tempf5$degF" : "---";

# send html page to browser
print <<EOF;
<!DOCTYPE html>
<html><head><title>$title</title></head>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.4/Chart.min.js"></script>
<body>
<canvas id="myChart" style="width:100%;max-width:1900px"></canvas>

<script>
const xValues = [$x];

new Chart("myChart", {
  type: "line",
  data: {
    labels: xValues,
    datasets: [
      { label: "$name0", data: [$y0], borderColor: "red",    fill: false }
     ,{ label: "$name1", data: [$y1], borderColor: "orange", fill: false }
     ,{ label: "$name2", data: [$y2], borderColor: "green",  fill: false }
     ,{ label: "$name3", data: [$y3], borderColor: "teal",   fill: false }
     ,{ label: "$name4", data: [$y4], borderColor: "blue",   fill: false }
     ,{ label: "$name5", data: [$y5], borderColor: "violet", fill: false }
    ]
  },
  options: {
    title: {
      display: true,
      text: "$header",
      fontSize: 16,
      fontColor: '#a8f'
    },
    legend: {display: true},
    spanGaps: true,
    tooltips: {
      titleFontSize: 16,
      bodyFontSize: 16,
      displayColors: false,
      callbacks: {
        label: function(tooltipItem, data) {
          var label = data.datasets[tooltipItem.datasetIndex].label || '';
          if (label) { label += ': '; }
          label += tooltipItem.yLabel;
          label += '$degC / ';
          label += Math.round(tooltipItem.yLabel * 18 + 320) / 10;
          label += '$degF';
          return label;
        }
      }
    }
  }
});
</script>
</body>
</html>
EOF
;
exit;
