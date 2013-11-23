#!/bin/bash

ALL_PERIOD_IDS="$(seq 1 12)"
FIRST_PERIOD_ID=1
BASE_URL=https://127.0.0.1
FIRST_DATE=2013-05-01
LAST_DATE=2013-10-05
ALL_TYPES=
ALL_AGENTS=
ALL_STATUSES=
COOKIES=/tmp/cookies.txt

usage(){
  echo "
Usage: $0 username password 

   --url      The server url
   --stats    Include stats per period
   --lists    Include reservations per period, and agent for REGULAR visitors
   --sum      Aggregate results
   --all      Enable stats, lists, and sum
   --periods  Space separated list of period IDs (default 1)
   --start    Starting date (default 2013-05-01)
   --end      Ending date (default 2013-10-05)
   --types    The reservation type (0..5)
   --agents   The reservation agent (0..7) 
   --statuses The reservation status (0..4)

"
  exit 1
}
if [  $# -lt 2 ]; then
  usage
fi

TEMP=$(getopt -o h --long help,output:,agents:,types:,statuses:,start:,end:,sum,all,periods:,stats,lists,url: -n 'get_cvs.sh' -- "$@")

if [ $? != 0 ] ; then echo "Terminating..." >&2 ; exit 1 ; fi

eval set -- "$TEMP"

while true ; do
  case "$1" in
    -h|--help) usage ;;
    --lists) LISTS=true ; shift ;;
    --stats) STATS=true ; shift ;;
    --sum) SUM=true ; shift ;;
    --all) PERIODS="$ALL_PERIOD_IDS" ; shift ;;
    --periods) PERIODS="$2" ; shift 2;;
    --agents) AGENTS="$2" ; shift 2;;
    --types) TYPES="$2" ; shift 2;;
    --statuses) STATUSES="$2" ; shift 2;;
    --start) FIRST_DATE=$2 ; shift 2;;
    --end) LAST_DATE=$2 ; shift 2;;
    --url) URL=$2 ; shift 2;;
    --output) OUTPUT=$2 ; shift 2;;
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
: ${OUTPUT:=}

if [ -n "$OUTPUT" ]; then
  exec 1>$OUTPUT
  exec 2>/dev/null
fi

stat $COOKIES && rm $COOKIES

curl -s -c $COOKIES -b $COOKIES $URL/accounts/login/ -k -o /dev/null &>/dev/null
csrftoken=$(grep csrftoken $COOKIES | awk '{ print $7 }')
curl -s -c $COOKIES -b $COOKIES -d "username=$1&password=$2&csrfmiddlewaretoken=$csrftoken" $URL/accounts/login/ -k

if $LISTS; then
  for period in $PERIODS; do
      for rtype in $TYPES; do
        for agent in $AGENTS; do
          for status in $STATUSES; do
            curl -k  -b $COOKIES  $URL/reservations/?period=$period\&rtype=$rtype\&agent=$agent\&status=$status\&cvs=on\&txt=on
	    echo; echo; echo;
	    sleep 1
          done
        done
      done
  done
fi

if $STATS; then
	for period in $PERIODS; do
	  curl -k  -b $COOKIES  $URL/stats/?period=$period\&cvs=on\&txt=on
	done
fi

if $SUM; then
	curl -k  -b $COOKIES  $URL/stats/?start=$FIRST_DATE\&end=$LAST_DATE\&fast=on\&cvs=on\&txt=on
fi
