#==================================================================#
# PROCESS USERS - modified from jsaxon/parks
# Cecile Murray
#==================================================================#

import pandas as pd
import pytz
import sys

timezone = {"new_york" : "Eastern", "los_angeles" : "Pacific", "chicago" : "Central", "houston" : "Central", "phoenix" : "Mountain",
            "philadelphia" : "Eastern", "san_antonio" : "Central", "san_diego" : "Pacific", "dallas" : "Central", "san_jose" : "Pacific",
            "austin" : "Central", "jacksonville" : "Eastern", "san_francisco" : "Pacific", "columbus" : "Eastern", "fort_worth" : "Central",
            "indianapolis" : "Eastern", "charlotte" : "Eastern", "seattle" : "Pacific", "denver" : "Mountain", "washington" : "Eastern"}

# geofiles  = "/home/jamessaxon/parks/"
processed = "processed/"
geofiles  = "" 
city      = sys.argv[1]

print(city, "::", end = " ", flush = True)

users = []
# for x in "0123456789abcdef":
   
#    print(x, flush = True, end = " ")
   
df = pd.read_csv(processed + "/{}_000.csv".format(city), # nrows = 100000, 
                  names = ["uid", "ts", "geo", "lat", "lon", "acc", "hway"])

df.sort_values(by = ["uid", "ts"], inplace = True)
df.drop_duplicates(inplace = True)
df.drop(df[df.hway == 1].index, inplace = True)
df.drop(df[df.acc > 500].index, inplace = True)

df.ts = pd.to_datetime(df.ts, unit = "s").dt.tz_localize('utc').dt.tz_convert(pytz.timezone('US/' + timezone[city]))
df["date"] = df.ts.dt.date.astype(str)

home = df.loc[df.ts.dt.hour < 6, ["uid", "geo", "ts"]].copy()
home = home.groupby(["uid", "geo"]).count().reset_index().sort_values(["uid", "ts"], ascending = [True, False])
home = home[home.ts > 1].drop_duplicates("uid") # the user must have more than one night-time ping there.
home = home[["uid", "geo"]].rename(columns = {"geo" : "home"})

df = pd.merge(df, home)

users.append(home)

users = pd.concat(users)
users.to_csv(processed + "/{}_users.csv".format(city), index = False)

import geopandas as gpd

boundary = gpd.read_file(geofiles + "places/{}.geojson".format(city))
tracts   = gpd.read_file(geofiles + "tracts/{}.geojson".format(city))
tracts["geoid"] = tracts.STATEFP + tracts.COUNTYFP + tracts.TRACTCE
# tracts = list(tracts.loc[tracts.within(boundary.ix[0].geometry), "geoid"])

# tracts = users.loc[users.home.isin(tracts), ["home"]].groupby("home").mean()
# # tracts = tracts[(tracts.index // 1000000) == 17031]
# tracts.to_csv(processed + "/{}_tracts.csv".format(city), index = True, float_format = "%.5f")