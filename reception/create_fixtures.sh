echo -e "[\n"

let pk=1

############## B #######################

values="B 1 71 2
Z 1 32 2
M1 101 105 14
M1 201 205 8
M2 101 112 3
M2 201 212 4
M3 101 107 3
M3 201 234 2
M3 301 331 14
M4 101 109 2
M4 201 209 5
M5 101 109 5
M5 201 209 5"

echo "$values" | while read area start end category; do
  for i in $(seq $start $end); do
  cat <<EOF
{ "model": "reception.Appartment", "pk":$pk, "fields": { "area": "$area", "no": "$i", "category": "$category" } },
EOF
let pk++
  done
done

echo "]"
