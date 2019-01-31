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

# setup
datadir = "processed/"
shpdir = "tracts/"
city = sys.argv[1]
pylab.ion()

# read in data
df = pd.read_csv(datadir + city + "_users.csv")
fulldf = pd.read_csv(datadir + city + "_000.csv", columns = ["uid", "timestamp", "tract", "lat", "lon", "acc", "hwy"])
map_df = gpd.read_file(shpdir + city + ".geojson")

# hey look, it's a city
map_df.plot()

# collapse this weird 11-tract data frame
sumdf = df.groupby('home', as_index=False).agg('count')
sumdf.home = sumdf['home'].astype(str)

# now merge in data
merged = map_df.merge(sumdf, left_on = "GEOID", right_on = "home")
merged.plot(column = "uid")

# okay now let's do it with the bigger one
aggdf = fulldf.groupby('home', as_index=False).agg('count')
aggdf