#!/bin/bash

ALL_PERIOD_IDS=$(seq 1 12)
FIRST_PERIOD_ID=1
BASE_URL=https://192.168.1.124
FIRST_DATE=2013-05-01
LAST_DATE=2013-10-05
ALL_TYPES=0
ALL_AGENTS=0\ 1\ 2
ALL_STATUSES=3

usage(){
  echo "
Usage: $0 username password 

   --stats   Include stats per period
   --lists   Include reservations per period, and agent for REGULAR visitors
   --sum     Aggregate results
   --all     Enable stats, lists, and sum
   --periods Space separated list of period IDs (default 1)
   --start   Starting date (default 2013-05-01)
   --end     Ending date (default 2013-10-05)
   --url     The server url
   
"
  exit 1
}
if [  $# -lt 2 ]; then
  usage
fi

TEMP=$(getopt -o h --long help,agents:,types:,statuses:,start:,end:,sum,all,periods:,stats,lists,url: -n 'get_cvs.sh' -- "$@")

if [ $? != 0 ] ; then echo "Terminating..." >&2 ; exit 1 ; fi

eval set -- "$TEMP"

while true ; do
  case "$1" in
    -h|--help) usage ;;
    --lists) LISTS=true ; shift ;;
    --stats) STATS=true ; shift ;;
    --sum) SUM=true ; shift ;;
    --all) PERIODS=$ALL_PERIOD_IDS ; shift ;;
    --periods) PERIODS=$2 ; shift 2;;
    --agents) AGENTS=$2 ; shift 2;;
    --types) TYPES=$2 ; shift 2;;
    --statuses) STATUS=$2 ; shift 2;;
    --start) FIRST_DATE=$2 ; shift 2;;
    --end) LAST_DATE=$2 ; shift 2;;
    --url) URL=$2 ; shift 2;;
    --) shift ; break ;;
    *) echo "Internal error!" ; usage ;;
  esac
done

: ${STATS:=false}
: ${LISTS:=false}
: ${SUM:=false}
: ${URL:=$BASE_URL}
: ${PERIODS:=$FIRST_PERIOD_ID}
: ${AGENTS:=$ALL_AGENTS}
: ${TYPES:=$ALL_TYPES}
: ${STATUSES:=$ALL_STATUSES}

curl -s -c cookies.txt -b cookies.txt $URL/accounts/login/ -k -o /dev/null
csrftoken=$(grep csrftoken cookies.txt | awk '{ print $7 }')
curl -s -c cookies.txt -b cookies.txt -d "username=$1&password=$2&csrfmiddlewaretoken=$csrftoken" $URL/accounts/login/ -k

for period in $PERIODS; do
  for rtype in $TYPES; do
    for agent in $AGENTS; do
      for status in $STATUSES; do
      if $LISTS; then
	curl -k  -b cookies.txt  $URL/reservations/?period=$period\&rtype=$rtype\&agent=$agent\&status=$status\&cvs=on
	echo; echo; echo;
	sleep 1
      fi
done
done
done
done

if $STATS; then
        echo "Period+++Start+++End+++Total+++Euro+++B3+++EA+++MY+++DAILY+++UNIT+++OSSEAY"
	for period in $PERIODS; do
	  curl -k  -b cookies.txt  $URL/stats/?period=$period\&cvs=on
	done
fi

if $SUM; then
        echo "Period+++Start+++End+++Regular+++Euro+++B3+++EA+++MY+++DAILY+++UNIT+++OSSEAY\n"
	curl -k  -b cookies.txt  $URL/stats/?start=$FIRST_DATE\&end=$LAST_DATE\&fast=on\&cvs=on
fi
