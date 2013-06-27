echo -e "[\n"

let pk=1

############## B #######################

values="Β 1 71 2
Ζ 1 32 2
Μ1 101 105 14
Μ1 201 205 8
Μ2 101 112 3
Μ2 201 212 4
Μ3 101 107 3
Μ3 201 234 2
Μ3 301 331 14
Μ4 101 109 2
Μ4 201 209 5
Μ5 101 109 5
Μ5 201 209 5
Α 1 1 5"

echo "$values" | while read area start end category; do
  for i in $(seq $start $end); do
  cat <<EOF
{ "model": "reception.Appartment", "pk":$pk, "fields": { "area": "$area", "no": "$i", "category": "$category" } },
EOF
let pk++
  done
done

echo "]"
