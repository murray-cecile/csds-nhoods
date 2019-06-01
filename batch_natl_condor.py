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
request_memory = 8GB
Requirements = OSGVO_OS_STRING == "RHEL 7"
# Executable and inputs
executable              = /home/cmmurray/stash/test-state.sh 
initialdir              = /stash/user/cmmurray
# Save your work.
ShouldTransferFiles     = YES
when_to_transfer_output = ON_EXIT

# Send the job to Held state on failure. 
on_exit_hold = (ExitBySignal == True) || (ExitCode != 0)

# Periodically retry the jobs every 10 minutes, up to a maximum of 5 retries.
periodic_release =  (NumJobStarts < 5) && ((CurrentTime - EnteredCurrentStatus) > 600)

# requirements per Lincoln
Requirements = OSGVO_OS_STRING == "RHEL 7"
"""

job = """
log    = /stash/user/cmmurray/condor/uid-st/{}.{}.$(Cluster).log
error  = /stash/user/cmmurray/condor/uid-st/{}.{}.$(Cluster).err
output = /stash/user/cmmurray/condor/uid-st/{}.{}.$(Cluster).out
transfer_input_files    = miniconda.sh, condarc, process_single_job.py, make_csv_exist.py, liveramp/{}.csv.bz2, geo/ways/{}_way.geojson, geo/tracts/us_tracts.geojson
transfer_output_files   = {}_{}.csv.bz2
transfer_output_remaps  = "{}_{}.csv.bz2 = processed/{}/{}.csv.bz2"
args                    = {} {}
queue
"""

STATES = ["01", "04", "05", "06", "08", "02", "09", "10", "11", "12", "13",
 "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27",
  "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40",
  "41", "42", "44", "45", "46", "47", "48", "49", "50", "51", "53", "54", "55", "56"]


UID_LIST = ['u_' + x + y for x in "0123456789abcdef" for y in "0123456789abcdef"]

def main(st_list, filename, uid_list):

  # print(uid_list == True)

  if not uid_list[0]:
    uid_list = UID_LIST
  
  if not st_list:
    st_list = STATES

  for j in uid_list:

    print(j)
    if not os.path.exists('processed/{}'.format(j)):
        os.makedirs('processed/{}'.format(j))
        print('processed/{}'.format(j))

    if os.path.exists('processed/{}/{}.csv.bz2'.format(j, st)):
      print("u_{} {} already exists".format(j, st))

      with open(filename, "a") as out:

        out.write(header)
        out.write(job.format(j, st, j, st, j, st, j, st, j, st, j, st, j, st, j[2:4], st))

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-st", "--st", nargs='+', help="State fips code")
    parser.add_argument('-f', "--file",help='Condor submit filename')
    parser.add_argument('-j', '--uid', nargs='+')
    args = parser.parse_args()


    main(st_list = args.st, filename = args.file, uid_list = args.uid)    
