#=========================================================================#
# CONCATENATE ACROSS JOBS
# Merge all user id files for a single state, drop imprecise
#
# Cecile Murray
#=========================================================================#

import pandas as pd 
import argparse


UID_LIST = [x + y for x in "0123456789abcdef" for y in "0123456789abcdef"]

STATE_LIST = ["01", "04", "05", "06", "08", "02", "09", "10", "11", "12", "13",
 "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27",
  "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40",
  "41", "42", "44", "45", "46", "47", "48", "49", "50", "51", "53", "54", "55", "56"]



def main(st_list, uid_list, suffix):

  print(st_list, uid_list)

  if not uid_list:
    uid_list = UID_LIST

  if not st_list:
    st_list = STATE_LIST

  for j in uid_list:
    for st in st_list:

      print('u_{}/{}.csv.bz2'.format(j, st))
      df = pd.read_csv('u_{}/{}.csv.bz2'.format(j, st), 
                      names = ["uid", "ts", "tract", "lat", "lon", "acc", "hway"],
                      dtype = {'uid': str, 'ts': int, 'tract': str, 'lat': float, 'lon': float, 'acc': int, 'hway': int})
      # print(df.head())
      df.drop(df[df.uid == '0'].index, inplace = True) 
      df.drop(df[df.acc > 500].index, inplace = True)
      # print(df.head())
      df.to_csv('u_{}/u_{}{}.csv.bz2'.format(j, j, suffix), mode = 'a', index = False, float_format='%.5f', header = False, compression = 'bz2')

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-st", "--stlist", nargs='+', default = "11", help="state fips code list")
    parser.add_argument('-uids', "--uids", help="a list of uids", action='append')
    parser.add_argument('-suff', '--suffix', default = '', help = 'characters to append to file name')
    args = parser.parse_args()
    
    main(st_list = args.stlist, uid_list=args.uids, suffix = args.suffix)
