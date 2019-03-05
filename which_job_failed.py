#=========================================================================#
# CHECK WHICH CONDOR JOB FAILED
# Given a job # in a group of jobs, return which user id and state failed
#
# Cecile Murray
#=========================================================================#

import argparse

UID_LIST = [x + y for x in "0123456789abcdef" for y in "0123456789abcdef"]


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-job", "--job",  type = int, default = "", help="Job number")
    parser.add_argument("-uid-list", "--uids",  type = list, default = UID_LIST, help="Job number")
    args = parser.parse_args()

    uid = UID_LIST[args.job]
    if args.uids:
        uid = args.uids[args.job]


    print('Job #{} had uid {}'.format(args.job, uid))