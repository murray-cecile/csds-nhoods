
cd ~/stash

find processed/ -type f -empty | grep -o u_[[:alnum:]]/$1* > failed-jobs-$1.txt
cat failed-jobs-$1.txt | grep -o u_[[:alnum:]] > user-ids.txt
python batch_natl_condor.py -st $1 -file resubmit-holds-$1.submit -j $(cat user-ids.txt)