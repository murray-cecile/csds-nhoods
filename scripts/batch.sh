
#!/bin/bash 

# from Jamie
cat [0-4]??.csv | awk '{ print > "u_"substr($1,1,1)".csv" }'

# mkdir sorted




bzcat /home/jsaxon/LiveRampReduce/LR_499.csv.bz2 | awk '{print >> "sorted/u_"substr($1,6,3)".csv" }'

# FINAL COMMAND
bzcat /home/jsaxon/LiveRampReduce/0-4]??.csv.bz2 | awk '{print >> "sorted/u_"substr($1,6,3)".csv" }'