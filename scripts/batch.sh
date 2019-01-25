
#!/bin/bash 

# Working out how to take the 500 .csv.bz2 files with the data, sort by user ID, and chunk into other CSVs.

# from Jamie
cat [0-4]??.csv | awk '{ print > "u_"substr($1,1,1)".csv" }'

# mkdir sorted

bzcat /home/jsaxon/LiveRampReduce/LR_499.csv.bz2 | awk '{print >> "sorted/u_"substr($1,6,3)".csv" }'

bzcat /home/jsaxon/LiveRampReduce/LR_499.csv.bz2 | awk '{print >> "sorted/u_"substr($1,6,2)".csv" }'

# FINAL COMMAND
# bzcat /home/jsaxon/LiveRampReduce/0-4]??.csv.bz2 | awk '{print >> "sorted/u_"substr($1,6,3)".csv" }'