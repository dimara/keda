#!/bin/bash

if [ $# -lt 2 ]; then
  echo "Usage: $0 user password [year] [output dir]"
  exit 1
fi


USER=$1
PASSWD=$2
YEAR=$3
OUTPUTDIR=$4

: ${YEAR:=2013}
: ${OUTPUTDIR:=lists}

mkdir -p $OUTPUTDIR/$YEAR

for p in {1..12}; do
   for a in {0..2}; do 
       ./get_cvs.sh --periods $p --types 0 --agents $a --statuses 3 --lists $USER $PASSWD > $OUTPUTDIR/$YEAR/period_$p-type_0-agent_$a-status_3.csv
   done
done
