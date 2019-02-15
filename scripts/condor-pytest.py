#!/usr/bin/env python

import os

header = """
universe = vanilla

# Executable and inputs
executable              = /home/cmmurray/condor-pytest.sh 
initialdir              = /stash/user/cmmurray/

# Save your work.
ShouldTransferFiles     = YES
when_to_transfer_output = ON_EXIT

"""

job = """
log    = /stash/user/cmmurray/post.$(Cluster).log
error  = /stash/user/cmmurray/post.$(Cluster).err
output = /stash/user/cmmurray/post.$(Cluster).out
transfer_input_files    = miniconda.sh, condarc
transfer_output_files   = pytest.csv
queue 
"""

with open("condor-post.submit", "w") as out:
    out.write(header)
    job.format("pytest")
~                      