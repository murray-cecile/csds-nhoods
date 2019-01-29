
#!/bin/bash 

# Working out how to take the 500 .csv.bz2 files with the data, sort by user ID, and chunk into other CSVs.

# from Jamie
# cat [0-4]??.csv | awk '{ print > "u_"substr($1,1,1)".csv" }'

# mkdir sorted

# this one took forever
# bzcat /home/jsaxon/LiveRampReduce/LR_499.csv.bz2 | awk '{print >> "sorted/u_"substr($1,6,3)".csv" }'

# running this one took about 7 min
# bzcat /home/jsaxon/LiveRampReduce/LR_499.csv.bz2 | awk '{print >> "sorted/u_"substr($1,6,2)".csv" }'

# FINAL COMMAND
# ran this in a script called awksort.sh on la2, using nohup
bzcat /home/jsaxon/LiveRampReduce/0-4]??.csv.bz2 | awk '{print >> "sorted2/u_"substr($1,6,2)".csv" }' 

# produced 258 files
ls  -lt sorted2 | wc -l
rm sorted2/u_1,.csv sorted2/u_sh.csv # remove file with obvs where user ids are missing + one with header rows

# count number of lines
cat sorted2/u_fe.csv | wc -l 
cat sorted2/u_fd.csv | wc -l

# nohup sh sortcleanup.sh > cleanup.out & 
# process 11268