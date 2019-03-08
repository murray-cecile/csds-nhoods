
# $1 is state

cd ~/stash

find processed/ -type f -empty | grep -o u_[[:alnum:]]/$1* > failed-jobs-$1.txt
python batch_natl_condor.py -st $1 -file 'resubmit-holds-$1.submit' -j $(> failed-jobs-$1.txt)