#==================================================================#
# IDENTIFY HOME LOCATIONS
# ID overnight locations
#
# Cecile Murray
#==================================================================#

import pandas as pd 

GEODIR = 'geo/'
PROCESSED = 'processed/'

## TO DO: TIMEZONES


uid_list = [x + y for x in "0123456789abcdef" for y in "0123456789abcdef"]

for u in uid_list:

    df = pd.read_csv(PROCESSED + "u_{}.csv.bz2".format(u), # nrows = 100000, 
                    names = ["uid", "ts", "geo", "lat", "lon", "acc", "hway"])

    df.sort_values(by = ["uid", "ts"], inplace = True)
    df.drop_duplicates(inplace = True)
    df.drop(df[df.hway == 1].index, inplace = True)
    df.drop(df[df.acc > 500].index, inplace = True)

    # need to localize all these timezones
    df.ts = pd.to_datetime(df.ts, unit = "s").dt.tz_localize('utc').dt.tz_convert(pytz.timezone('US/' + timezone[city]))
    df["date"] = df.ts.dt.date.astype(str)

    home = df.loc[df.ts.dt.hour < 6, ["uid", "geo", "ts"]].copy()
    home = home.groupby(["uid", "geo"]).count().reset_index().sort_values(["uid", "ts"], ascending = [True, False])
    home = home[home.ts > 1].drop_duplicates("uid") # the user must have more than one night-time ping there.
    home = home[["uid", "geo"]].rename(columns = {"geo" : "home"})

    df = pd.merge(df, home)

    users.append(home)

    users = pd.concat(users)
    users.to_csv(PROCESSED + "/{}_users.csv".format(u), index = False)