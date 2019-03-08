#==================================================================#
# IDENTIFY HOME LOCATIONS
# ID overnight locations
#
# Cecile Murray
#==================================================================#

import pandas as pd 
import pytz
from pytz import timezone
import argparse


GEODIR = ''
PROCESSED = ''


# list of timezones by county for all 3,143 counties

def change_tz(row):
    ''' converts timestamp in row to correct timezone 
        returns the converted time and the hour separately so that we can identify night in local time
    '''

    ts = pd.to_datetime(row.ts, unit = 's').tz_localize('utc').tz_convert(pytz.timezone(row.tz))
    return pd.Series([ts, ts.hour])

def locate_homes(df, st):
    '''locate modal night time location for users, count visits to each tract write to csv
        return main df with home locations merged in'''

    # IDENTIFY HOMES
    home = df.loc[df.hour < 6, ["uid", "tract", "ts"]].copy()
    home = home.groupby(["uid", "tract"]).count().reset_index().sort_values(["uid", "ts"], ascending = [True, False])
    home = home[home.ts > 1].drop_duplicates("uid") # the user must have more than one night-time ping there.
    home = home[["uid", "tract"]].rename(columns = {"tract" : "home"})

    rv = pd.merge(df, home)

    visits = df.groupby(['uid', 'tract']).count().reset_index()
    visits = visits[['uid', 'tract', 'ts']].rename(columns={'ts':'visits'})
    visits = visits.join(home[['uid', 'home']].set_index("uid"), on="uid")
    visits['home'] = visits['home'] == visits['tract']
    visits.to_csv(PROCESSED +  'all_{}_visits.csv.bz2'.format(st), index = False,  float_format='%.5f', compression = 'bz2')
    print("done writing visits")

    return rv


def main(st):
    ''' 
        - read in each file 
        - sort by user id and timestamp, drop duplicates and observations on roads
        - localize timezones so we can identify where people are between 12am and 6am
        - identify homes by pings at these nighttime locations
        - count visits
        - write files
    '''
    
    df = pd.read_csv(PROCESSED + 'all_{}.csv.bz2'.format(st), # nrows = 100000, 
                    names = ["uid", "ts", "tract", "lat", "lon", "acc", "hway"],
                    dtype = {'uid': str, 'ts': int, 'tract': str, 'lat': float, 'lon': float, 'acc': int})

    df.sort_values(by = ["uid", "ts"], inplace = True)
    df.drop_duplicates(inplace = True)
    df.drop(df[df.hway == 1].index, inplace = True)

    print("df size is now:", df.shape)

    # need to localize all these timezones - THIS IS REALLY SLOW
    timezones = pd.read_csv(GEODIR + 'countytimezones.csv', dtype = {'stcofips': 'str', 'tz': 'str'})

    df['stcofips'] = df['tract'].astype('str').str.slice(0,5)
    df = df.join(timezones.set_index('stcofips'), on = 'stcofips', how = 'left')
    df[['ts', 'hour']] = df.apply(change_tz, axis = 1)
    print("got through timezones")
    print(df.head())
    df.drop(columns=['stcofips'])

    # lastly, locate homes, count visits, etc
    df = locate_homes(df, st)



if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-st", "--st",  type = str, default = "11", help="state FIPS code")
    # parser.add_argument("-j", "--job", default = "00", help="two-digit user id" )
    args = parser.parse_args()

    main(st = args.st)