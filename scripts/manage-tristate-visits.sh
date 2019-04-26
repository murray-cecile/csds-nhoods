
cd ~/stash

# remove old files
rm failed-tristate-jobs.txt resubmit-visits.submit

find processed/uids -type f -empty | grep ILMNWI_visits* > failed-tristate-jobs.txt
cat failed-tristate-jobs.txt | grep -o 'u_[a-z0-9]\{2\}' | grep -o '[a-z0-9]\{2\}' > user-ids.txt
python condor-locate-homes.py -st 17 27 55 -f resubmit-visits.submit -uids $(cat user-ids.txt) -suff _ILMNWI