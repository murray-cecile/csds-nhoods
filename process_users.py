#==================================================================#
# PROCESS USERS - copy from jsaxon/parks
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
geofiles  = "./parks/" 
city      = sys.argv[1]

print(city, "::", end = " ", flush = True)

users, parks, museums, stadia = [], [], [], []
for x in "0123456789abcdef":
   
   print(x, flush = True, end = " ")
   
   df = pd.read_csv("u_{}.csv".format(x), # nrows = 100000, 
                    names = ["uid", "ts", "geo", "lat", "lon", "acc", "park", "muse", "stad", "hway"])

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
         
   home = home.merge(park_visits.reset_index(), how = "left")
   home = home.merge(museum_visits.reset_index(), how = "left")
   home = home.merge(stadium_visits.reset_index(), how = "left")
   
   home.npark = home.npark.fillna(0).astype(int)
   home.nmuse = home.nmuse.fillna(0).astype(int)
   home.nstad = home.nstad.fillna(0).astype(int)
   
   users.append(home)


   # All pings from each user are in the same file, 
   #   so we can count by file and then sum those counts.
   parks.append(df.loc[df.park >= 0].drop_duplicates(["home", "park", "uid", "date"])\
                  .rename(columns = {"home" : "geoid", "uid" : "nusers"})\
                  .groupby(["park", "geoid"]).nusers.count().reset_index())
   
   museums.append(df.loc[df.muse >= 0].drop_duplicates(["home", "muse", "uid", "date"])\
                    .rename(columns = {"home" : "geoid", "uid" : "nusers"})\
                    .groupby(["muse", "geoid"]).nusers.count().reset_index())

   stadia.append(df.loc[df.stad >= 0].drop_duplicates(["home", "stad", "uid", "date"])\
                   .rename(columns = {"home" : "geoid", "uid" : "nusers"})\
                   .groupby(["stad", "geoid"]).nusers.count().reset_index())


pd.concat(parks)  .groupby(["park", "geoid"]).nusers.sum().reset_index().to_csv("parks.csv",   index = False)
pd.concat(museums).groupby(["muse", "geoid"]).nusers.sum().reset_index().to_csv("museums.csv", index = False)
pd.concat(stadia) .groupby(["stad", "geoid"]).nusers.sum().reset_index().to_csv("stadia.csv",  index = False)


users = pd.concat(users)
users.to_csv("users.csv", index = False)

import geopandas as gpd

boundary = gpd.read_file(geofiles + "places/{}.geojson".format(city))
tracts   = gpd.read_file(geofiles + "tracts/{}.geojson".format(city))
tracts["geoid"] = tracts.STATEFP + tracts.COUNTYFP + tracts.TRACTCE
tracts = list(tracts.loc[tracts.within(boundary.ix[0].geometry), "geoid"])

tracts = users.loc[users.home.isin(tracts), ["home", "npark", "nmuse", "nstad"]].groupby("home").mean()
# tracts = tracts[(tracts.index // 1000000) == 17031]
tracts.to_csv("tracts.csv", index = True, float_format = "%.5f")