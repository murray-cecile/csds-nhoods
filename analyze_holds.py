# write job status to a csv

import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("-id", "--idnum",  help="Condor ID number")
args = parser.parse_args()

holds = pd.read_csv('hold.csv', skipfooter=3)
holds.to_csv('holds_{}.csv'.format(args.idnum))    
