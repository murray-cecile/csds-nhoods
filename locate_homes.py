#==================================================================#
# IDENTIFY HOME LOCATIONS
# ID overnight locations
#
# Cecile Murray
#==================================================================#

import pandas as pd 
import pytz
from pytz import timezone


GEODIR = 'data/'
PROCESSED = 'processed/'

# list of timezones by county for all 3,143 counties
timezones = pd.read_csv(GEODIR + 'countytimezones.csv', dtype = {'stcofips': 'str', 'tz': 'str'})

def change_tz(row):
    ''' converts timestamp in row to correct timezone '''

    return pd.to_datetime(row.ts, unit = 's').tz_localize('utc').tz_convert(pytz.timezone(row.tz))


if __name__ == "__main__":
    
    uid_list = [x + y for x in "0123456789abcdef" for y in "0123456789abcdef"]

    for u in uid_list:

        df = pd.read_csv(PROCESSED + 'u000.csv', # nrows = 100000, 
                        names = ["uid", "ts", "geo", "lat", "lon", "acc", "hway"])

        df.sort_values(by = ["uid", "ts"], inplace = True)
        df.drop_duplicates(inplace = True)
        df.drop(df[df.hway == 1].index, inplace = True)


        # need to localize all these timezones
        df['stcofips'] = df['geo'].astype('str').str.slice(0,5)
        df = df.join(timezones.set_index('stcofips'), on = 'stcofips', how = 'left')
        df['ts'] = df.apply(change_tz, axis = 1)
        df["date"] = df.ts.dt.date.astype(str)

        home = df.loc[df.ts.dt.hour < 6, ["uid", "geo", "ts"]].copy()
        home = home.groupby(["uid", "geo"]).count().reset_index().sort_values(["uid", "ts"], ascending = [True, False])
        home = home[home.ts > 1].drop_duplicates("uid") # the user must have more than one night-time ping there.
        home = home[["uid", "geo"]].rename(columns = {"geo" : "home"})

        df = pd.merge(df, home)

        users.append(home)

        users = pd.concat(users)
        users.to_csv(PROCESSED + "/{}_users.csv".format(u), index = False)