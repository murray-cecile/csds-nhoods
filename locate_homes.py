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


GEODIR = 'data/'
PROCESSED = 'processed/'
INFILE = 'u_00.csv.bz2'
HOMEFILE = '00_homes.csv'
VISITSFILE = "00_visits.csv"
TRACTSFILE = "00_tracts.csv"


# list of timezones by county for all 3,143 counties

def change_tz(row):
    ''' converts timestamp in row to correct timezone 
        returns the converted time and the hour separately so that we can identify night in local time
    '''

    ts = pd.to_datetime(row.ts, unit = 's').tz_localize('utc').tz_convert(pytz.timezone(row.tz))

    return pd.Series([ts, ts.hour])

def main(user_id):
    ''' 
        - read in each file 
        - sort by user id and timestamp, drop duplicates and observations on roads
        - localize timezones so we can identify where people are between 12am and 6am
        - identify homes by pings at these nighttime locations
        - count visits
        - write files
    '''
    
    df = pd.read_csv(PROCESSED + INFILE, # nrows = 100000, 
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
    print(df.head())
    # df["date"] = df.ts.dt.date.astype(str)
    df.drop(columns=['stcofips'])


    # IDENTIFY HOMES
    home = df.loc[df.hour < 6, ["uid", "tract", "ts"]].copy()
    home = home.groupby(["uid", "tract"]).count().reset_index().sort_values(["uid", "ts"], ascending = [True, False])
    home = home[home.ts > 1].drop_duplicates("uid") # the user must have more than one night-time ping there.
    home = home[["uid", "tract"]].rename(columns = {"tract" : "home"})

    df = pd.merge(df, home)

    # sum up the number of visits by each user to each tract
    visits = df.groupby(['uid', 'tract']).count().reset_index()
    visits = visits[['uid', 'tract', 'ts']].rename(columns={'ts':'visits'})
    
    # count the number of observations and number of home visits for each user
    home['obvs'] = df.groupby(['uid']).count().reset_index().ts
    home['visits'] = df[df.tract == df.home].groupby(['uid', 'home']).count().reset_index().ts

    # count the number of visits to each tract
    tracts = df.groupby(['tract']).nunique()
    tracts = tracts[['ts']].rename(columns={'ts':'visits'}).reset_index()

    # write to file
    home.to_csv(PROCESSED +  HOMEFILE, index = False)
    visits.to_csv(PROCESSED +  VISITSFILE, index = False)
    tracts.to_csv(PROCESSED + TRACTSFILE, index = False)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-j", "--uid",  type = str, default = "01", help="Two-digit user id")
    args = parser.parse_args()

    # main(user_id = args.uid)

 
    df = pd.read_csv(PROCESSED + INFILE, # nrows = 100000, 
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
    print(df.head())
    # df["date"] = df.ts.dt.date.astype(str)
    df.drop(columns=['stcofips'])


    # IDENTIFY HOMES
    home = df.loc[df.hour < 6, ["uid", "tract", "ts"]].copy()
    home = home.groupby(["uid", "tract"]).count().reset_index().sort_values(["uid", "ts"], ascending = [True, False])
    home = home[home.ts > 1].drop_duplicates("uid") # the user must have more than one night-time ping there.
    home = home[["uid", "tract"]].rename(columns = {"tract" : "home"})

    df = pd.merge(df, home)

    # sum up the number of visits by each user to each tract
    visits = df.groupby(['uid', 'tract']).count().reset_index()
    visits = visits[['uid', 'tract', 'ts']].rename(columns={'ts':'visits'})
    
    # count the number of observations and number of home visits for each user
    home['obvs'] = df.groupby(['uid']).count().reset_index().ts
    home['visits'] = df[df.tract == df.home].groupby(['uid', 'home']).count().reset_index().ts

    # count the number of visits to each tract
    tracts = df.groupby(['tract']).nunique()
    tracts = tracts[['ts']].rename(columns={'ts':'visits'}).reset_index()
