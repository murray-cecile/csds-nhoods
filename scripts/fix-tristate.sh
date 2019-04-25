cd ~/stash/processed

uid_list="00 01 02 03 04 05 06 07 10"

for uid in $uid_list; do

    echo u_$uid
    rm u_$uid/u_$uid"_ILMNWI.csv.bz2"

done 

nohup python concatenate_jobs.py -suff _ILMNWI -st 17 27 55 -uids $uid_list  > fix-tristate.out &