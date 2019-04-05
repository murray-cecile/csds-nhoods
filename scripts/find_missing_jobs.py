
import os
import argparse

UID_LIST = [x + y for x in "0123456789abcdef" for y in "0123456789abcdef"]

STATES = ["01", "04", "05", "06", "08", "02", "09", "10", "11", "12", "13",
 "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27",
  "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40",
  "41", "42", "44", "45", "46", "47", "48", "49", "50", "55"]  #"51", "53", "54", "55", "56"]

def print_missing(st_list):
    '''print missing user ids'''

    missing = {}

    if not st_list:
        st_list = STATES

    for u in UID_LIST:
        for st in STATES:

            missing[st] = []

            if not os.path.exists('u_{}/{}.csv.bz2'.format(u, st)):
                print('u_{}/{}.csv.bz2'.format(u, st))
                missing[st].append('u_{}'.format(u))
    
    print(missing)


def write_user_ids(st):
    ''' write missing user ids to text file'''

    missing = []

    for u in UID_LIST:

        if not os.path.exists('u_{}/{}.csv.bz2'.format(u, st)):
            print('u_{}/{}.csv.bz2'.format(u, st))
            missing[st].append('u_{}'.format(u))

            with open('missing-{}.txt'.format(st), "a") as f:
                f.write('u_{}'.format(u))


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-rec", "--rec", help="write list of user ids?")
    parser.add_argument("-st", "--st",  nargs='+', help="state fips code")
    args = parser.parse_args()
    
    if args.rec:
        write_user_ids(st = args.st)
    else: 
        print_missing(st_list = args.st)


