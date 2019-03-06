#==================================================================#
# BATCH NATIONAL JOIN JOB SUBMISSION FOR CONDOR
# creates the condor-post scripts for each of 256*51 jobs
#
# Cecile Murray
#==================================================================#

import os
import argparse

header = """
universe = vanilla
# Executable and inputs
executable              = /home/cmmurray/stash/locate-homes.sh 
initialdir              = /stash/user/cmmurray
# Save your work.
ShouldTransferFiles     = YES
when_to_transfer_output = ON_EXIT
"""

job = """
log    = /stash/user/cmmurray/condor/process_st_{}.$(Cluster).log
error  = /stash/user/cmmurray/condor/process_st_{}.$(Cluster).err
output = /stash/user/cmmurray/condor/process_st_{}.$(Cluster).out
transfer_input_files    = miniconda.sh, condarc, locate_homes.py, processed/states/all_{}.csv.bz2
transfer_output_files   = {}_homes.csv.bz2, {}_visits.csv.bz2, {}_tracts.csv.bz2
transfer_output_remaps  = "{}_homes.csv.bz2 = processed/states/{}_homes.csv.bz2", "{}_visits.csv.bz2 = processed/states/{}_visits.csv.bz2", "{}_tracts.csv.bz2 = processed/states/{}_tracts.csv.bz2"
args                    = {}
queue
"""

STATES = ["01", "04", "05", "06", "08", "02", "09", "10", "11", "12", "13",
 "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27",
  "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40",
  "41", "42", "44", "45", "46", "47", "48", "49", "50", "51", "53", "54", "55", "56"]


def main(st_list = STATES):

    for st in st_list:

        # # right now
        # if st == '50':
        #     continue

        with open('condor-process-states.submit', "a") as out:

            out.write(header)
            out.write(job.format(st, st, st, st, st, st, st, st, st, st, st, st, st, st))

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-st", "--st",  help="State fips code", action='append')
    args = parser.parse_args()

    main(st_list = args.st)    

