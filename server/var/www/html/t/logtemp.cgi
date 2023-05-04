#!/usr/bin/perl
# log data sent by rpi-ds18b20 temperature sensors logger

print "Content-type: text/html\n\n"; # must send this first or errors won't appear in browser

use CGI; # provides access to data received in GET/POST requests
$log      = "temp.log"; # store log in script directory
$query    = new CGI; # initialize CGI object
$tempdata = $query->param('t'); # read "t" parameter from query

open(LOG, ">>", $log) or die "Can't open log file $!"; # open log file in append mode
print LOG "$tempdata\n"; # write to log file
close (LOG);

print "OK\n"; # only for human testing, Curl on the RPi doesn't process this

exit;
