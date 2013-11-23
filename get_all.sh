#!/bin/bash

source /etc/default/keda


if [ $# -ne 2 ]; then
  echo "Usage: $0 <user> <password>"
  exit 1
fi

mkdir -p $OUTPUTDIR
rm $OUTPUTDIR/*

for p in {1..12}; do
  for a in {0..2}; do
    $SCRIPTS_DIR/get_cvs.sh --lists --periods $p --types 0 --agents $a --statuses 3 $1 $2 > $OUTPUTDIR/period_$p-rtype_0-agent_$a-status_3.csv
  done
done
