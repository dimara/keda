set terminal pdf enhanced
set output 'stats.pdf'

set style data histogram
set style histogram cluster gap 1
set datafile separator "|"
#set xtic rotate by -45

set style fill solid border rgb "black"
set auto x
set yrange [0:*]
plot 'stats.txt' using 4:xtic(1) title col, \
        '' using 5:xtic(1) title col, \
        '' using 6:xtic(1) title col, \
        '' using 7:xtic(1) title col, \
        '' using 8:xtic(1) title col, \
        '' using 9:xtic(1) title col, \
        '' using 10:xtic(1) title col
