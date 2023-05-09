#! /usr/bin/perl
# display chart from temp.log data (rev.20230509)
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
### end of user-defined variable ###

use CGI;      # provides access to GET/POST parameters from browser
$q = new CGI; # initialize CGI object

# by specifying days or hours, client can limit the chart size
$d = $q->param('days');  # get days value from query string
$h = $q->param('hours'); # get hours value from query string
if ($d) { $lines  = int((60/$minutes) * 60 * 24 * $d) }   # set number of lines per day to read from log
if ($h) { $lines += int((60/$minutes) * 60 * $h) }        # set number of lines per hours to read from log
unless ($lines) { $lines = int((60/$minutes) * 60 * 24) } # default to the last 24 hours if no value was provided

@log = `tail -n $lines $logfile`; # retrieve desired number of lines from log

# scan through each line of the log
foreach $line (@log) { chomp; # remove newline char
 ($date,$time,$temp0c,$temp1c,$temp2c,$temp3c) = split(" ",$line); # split array to read each value
 $x .= '"' . substr($date,5,5) . " " . substr($time,0,5) . '",';   # shorten date/time to "MM-DD hh:mm"
 # create arrays of values for each temp sensor
 $y0 .= $temp0c/1000 .','; # divide by 1000 to convert the celsius*1000 integers to floats
 $y1 .= ($temp1c ne "-") ? $temp1c/1000 .',' : ','; # if sensor couldn't be read the value in the log
 $y2 .= ($temp2c ne "-") ? $temp2c/1000 .',' : ','; # will be "-", in that case put empty value so that
 $y3 .= ($temp3c ne "-") ? $temp3c/1000 .',' : ','; # the point isn't plotted but still counted
}

# convert most recent temp values from C to F, for chart title
$temp1f = $temp1c*1.8/1000+32; 
$temp2f = $temp2c*1.8/1000+32;
$temp3f = $temp3c*1.8/1000+32;

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
    datasets: [{
      label: "$name0",
      data: [$y0],
      borderColor: "red",
      fill: false
    }, {.
      label: "$name1",
      data: [$y1],
      borderColor: "orange",
      fill: false
    }, {.
      label: "$name2",
      data: [$y2],
      borderColor: "green",
      fill: false
    }, {.
      label: "$name3",
      data: [$y3],
      borderColor: "teal",
      fill: false
    }]
  },
  options: {
    title: {
      display: true,
      text: "$name0: "+$temp0c/1000+"\\u00B0C - \
             $name1: "+$temp1c/1000+"\\u00B0C / $temp1f\\u00B0F - \
             $name2: "+$temp2c/1000+"\\u00B0C / $temp2f\\u00B0F - \
             $name3: "+$temp3c/1000+"\\u00B0C / $temp3f\\u00B0F",
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
          label += Math.round(tooltipItem.yLabel * 100) / 100;
          label += '\\u00B0C ';
          label += Math.round(tooltipItem.yLabel * 18 + 320) / 10;
          label += '\\u00B0F';
          return label;
        }
      }
    }
  }
});
</script>

EOF
;
exit;
