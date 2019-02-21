# !usr/bin/bash

cd /Users/cecilemurray/Documents/CSDS

# tracts - all US
# scp scripts/tracts.sh cmmurray@login.osgconnect.net:~/stash/geo
# scp tracts/us_tracts* cmmurray@login.osgconnect.net:~/stash/geo

# OSM ways file for each state
# scp ways/[0-9]*_way.geojson cmmurray@login.osgconnect.net:~/stash/geo/ways


scp batch_natl_condor.py process_single_job.py cmmurray@login.osgconnect.net:~/stash
