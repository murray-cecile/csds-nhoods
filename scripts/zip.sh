#!/bin/bash 

# bzipping all the csvs after the sort

# test one, purposefully keeping the input file
bzip2 sorted2/u_fe.csv -k

# for all
# nohup sh sortcleanup.sh > cleanup.out &