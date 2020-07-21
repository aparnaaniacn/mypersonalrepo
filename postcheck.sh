#!/bin/bash

function fail {
    printf '%s\n' "$*" >&2
    exit 1
}
echo $1
echo $2
a=`telnet $1 $2 </dev/null 2>&1 |grep Connected`
echo $a
test -n "$a" || echo "Telnet from nagios server failed."
#echo "nagios check success"
