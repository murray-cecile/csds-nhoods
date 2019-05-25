#=========================================================================#
# CONCATENATE TRISTATE VISIT MATRICES
# Merge all user id visit matrix files
#
# Cecile Murray
#=========================================================================#

import os
import pandas as pd 
import argparse


UID_LIST = [x + y for x in "0123456789abcdef" for y in "0123456789abcdef"]


def main(uid_list, suffix):

  print(uid_list)

  if not uid_list:
    uid_list = UID_LIST

  for j in uid_list:

    if not os.path.getsize('uids/u_{}_{}_visits.csv.bz2'.format(j, suffix)):
        continue

    else:

        print('uids/u_{}_{}_visits.csv.bz2'.format(j, suffix))
        df = pd.read_csv('uids/u_{}_{}_visits.csv.bz2'.format(j, suffix)) 
        df.to_csv('uids/visits_{}.csv.bz2'.format(suffix), mode = 'a', index = False, float_format='%.5f', header = False, compression = 'bz2')

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-uids', "--uids", nargs='+', help="a list of uids")
    parser.add_argument('-suff', '--suffix', default = '', help = 'characters to append to file name')
    args = parser.parse_args()
    
    main(uid_list=args.uids, suffix = args.suffix)
