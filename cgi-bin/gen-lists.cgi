#!/bin/bash

saveIFS=$IFS
IFS='=&'
parm=($QUERY_STRING)
IFS=$saveIFS


source /etc/default/keda

for ((i=0; i<${#parm[@]}; i+=2))
do
    declare var_${parm[i]}=${parm[i+1]}
done

echo Content-type: text/html
echo ""

cat <<EOF
<html>
  <head>
    <meta charset="utf-8">
  </head>
<body>
$(date)
<a href='/lists/results/latest'>See</a> the generated lists
</body>

EOF

exec >&-
exec 2>&-

$SCRIPTS_DIR/get_all.sh dimara marika
