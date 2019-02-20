#==================================================================#
# MAPPING STUFF
# Cecile Murray
#==================================================================#

import pandas as pd 
import geopandas as gpd
import numpy as np
import matplotlib
import sys
import pylab
import pytz

# setup
datadir = "processed/"
shpdir = "tracts/"
city = sys.argv[1]
pylab.ion()

timezone = {"new_york" : "Eastern", "los_angeles" : "Pacific", "chicago" : "Central", "houston" : "Central", "phoenix" : "Mountain",
            "philadelphia" : "Eastern", "san_antonio" : "Central", "san_diego" : "Pacific", "dallas" : "Central", "san_jose" : "Pacific",
            "austin" : "Central", "jacksonville" : "Eastern", "san_francisco" : "Pacific", "columbus" : "Eastern", "fort_worth" : "Central",
            "indianapolis" : "Eastern", "charlotte" : "Eastern", "seattle" : "Pacific", "denver" : "Mountain", "washington" : "Eastern"}


# read in data
df = pd.read_csv(datadir + city + "_users.csv")
fulldf = pd.read_csv(datadir + city + "_000.csv", names = ["uid", "timestamp", "tract", "lat", "lon", "acc", "hwy"])
map_df = gpd.read_file(shpdir + city + ".geojson")

# hey look, it's a city
# map_df.plot()

# collapse this weird 11-tract data frame
sumdf = df.groupby('home', as_index=False).agg('count')
sumdf.home = sumdf['home'].astype(str)

# now merge in data
merged = map_df.merge(sumdf, left_on = "GEOID", right_on = "home")
# merged.plot(column = "uid")

# okay now let's do it with the bigger one
aggdf = fulldf.groupby('tract', as_index=False).agg('count')
aggdf.tract = aggdf.tract.astype(str)
merged2 = map_df.merge(aggdf, left_on='GEOID', right_on = 'tract')
# merged2.plot(column = "uid")

fulldf['ts'] = pd.to_datetime(fulldf.timestamp, unit = "s").dt.tz_localize('utc').dt.tz_convert(pytz.timezone('US/' + timezone[city]))

fulldf.uid.unique()