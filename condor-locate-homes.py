#==================================================================#
# BATCH NATIONAL JOIN JOB SUBMISSION FOR CONDOR
# creates the condor-post scripts for each of 256 jobs
#
# Cecile Murray
#==================================================================#

import os
import argparse
import functools

header = """
universe = vanilla
# Executable and inputs
executable              = /home/cmmurray/stash/locate-homes.sh 
initialdir              = /stash/user/cmmurray
# Save your work.
ShouldTransferFiles     = YES
when_to_transfer_output = ON_EXIT

# Send the job to Held state on failure. 
on_exit_hold = (ExitBySignal == True) || (ExitCode != 0)

# Periodically retry the jobs every 10 minutes, up to a maximum of 5 retries.
periodic_release =  (NumJobStarts < 5) && ((CurrentTime - EnteredCurrentStatus) > 600)

# requirements 
Requirements = OSGVO_OS_STRING == "RHEL 7"
"""

job = """
log    = /stash/user/cmmurray/condor/process_u_{}.$(Cluster).log
error  = /stash/user/cmmurray/condor/process_u_{}.$(Cluster).err
output = /stash/user/cmmurray/condor/process_u_{}.$(Cluster).out
transfer_input_files    = miniconda.sh, condarc, locate_homes.py, processed/u_{}/u_{}{}.csv.bz2, countytimezones.csv
transfer_output_files   = u_{}{}_visits.csv.bz2
transfer_output_remaps  = "u_{}{}_visits.csv.bz2 = processed/uids/u_{}{}_visits.csv.bz2"
args                    = -j {} -st {} -suff {}
queue
"""

UID_LIST = [x + y for x in "0123456789abcdef" for y in "0123456789abcdef"]

STATE_LIST = ["01", "04", "05", "06", "08", "02", "09", "10", "11", "12", "13",
 "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27",
  "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40",
  "41", "42", "44", "45", "46", "47", "48", "49", "50", "51", "53", "54", "55", "56"]


def main(outfile, st_list, uid_list, suffix):

  if not st_list:
    st_list = STATE_LIST

  if not uid_list:
    uid_list = UID_LIST

  st_args = functools.reduce(lambda x, y: x + ' ' + y, st_list)
  print(st_args)

  for j in uid_list:

    with open(outfile, "a") as out:
        out.write(header)
        out.write(job.format(j, j, j, j, j, suffix, j, suffix, j, suffix, j, suffix, j, st_args, suffix)) #14 spots to fill rn?
 
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-uids', "--uids", nargs='+', help="a list of uids")
    parser.add_argument('-f', "--file", help="submission filename")
    parser.add_argument('-suff', '--suffix', default = '', help = 'characters to append to file name')
    parser.add_argument("-st", "--st", nargs='+', help="State fips code")
    args = parser.parse_args()

    main(outfile = args.file, st_list = args.st, uid_list = args.uids, suffix = args.suffix)    

