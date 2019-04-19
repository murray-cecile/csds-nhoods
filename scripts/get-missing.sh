
# $1 is state

cd ~/stash

rm resubmit-missing-$1.submit

python batch_natl_condor.py -st $1 -f resubmit-missing-$1.submit -j $(cat processed/missing-jobs.txt)
