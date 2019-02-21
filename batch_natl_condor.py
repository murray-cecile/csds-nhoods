#==================================================================#
# BATCH NATIONAL JOIN JOB SUBMISSION FOR CONDOR
# creates the condor-post scripts for each of 256*51 jobs
#
# Cecile Murray
#==================================================================#

import os

header = """
universe = vanilla
# Executable and inputs
executable              = /home/cmmurray/stash/test-state.sh 
initialdir              = /home/cmmurray/stash
# Save your work.
ShouldTransferFiles     = YES
when_to_transfer_output = ON_EXIT
"""

job = """
log    = /stash/users/cmmurray/condor/u_{:02d}.{}.$(Cluster).log
error  = /stash/users/cmmurray/condor/u_{:02d}.{}.$(Cluster).err
output = /stash/users/cmmurray/condor/u_{:02d}.{}.$(Cluster).out
transfer_input_files    = miniconda.sh, condarc, process_single_job.py, liveramp/u_{:02d}.csv.bz2, geo/tracts/us_tracts.shp, geo/ways/{}_way.geojson
transfer_output_files   = u_{:02d}_{}.csv
transfer_output_remaps  = "u_{:02d}_{}.csv = processed/u_{:02d}/{}.csv"
args                    = {:02d} {}
queue
"""

STATES = ["01", "04", "05", "06", "08", "02", "09", "10", "11", "12", "13",
 "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27",
  "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40",
  "41", "42", "44", "45", "46", "47", "48", "49", "50", "51", "53", "54", "55", "56"]


# output = 'stash/processed/{:02d}/{}.csv'.format(j, st)

for j in range(1,2):

  #   if j in [58, 403]: continue
  for st in STATES:

    with open('condor/condor-natl-{:02d}-{}.submit'.format(j, st), "w") as out:

      out.write(header)

      # if os.path.isfile(output.format(j, st)): #  and \
      #     # os.path.getsize(output.format(st, j)): 
      #     # continue
      #     print(j, st)

      out.write(job.format(j, st, j, st, j, st, j, st, j, st, j, st, j, st, j, st))
