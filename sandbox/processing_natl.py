#==================================================================#
# PROCESSING - version for whole country
# this was a terrible idea
# Cecile Murray
#==================================================================#

import geopandas as gpd
import pandas    as pd
import numpy     as np

from shapely.geometry import Point
import fiona.crs # from fiona.crs import from_espg raised an error

import os
import csv
import sys

# STATES = ["01", "02", "04", "05", "06", "08", "09", "10", "11", "12", "13",
#  "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27",
#   "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40",
#   "41", "42", "44", "45", "46", "47", "48", "49", "50", "51", "53", "54", "55", "56"]

STATES = ["01", "02", "04"]

def cut_box(row, *bounds):

  try:
    return bounds[0] < row.longitude < bounds[2] and \
           bounds[1] < row.latitude  < bounds[3]
  except TypeError:
    print(row)
    sys.exit()

def main(n = 0):

    # read in tract file
    tracts = gpd.read_file("tracts/us_tracts.shp")
    tracts = tracts[["GEOID", "geometry"]].rename(columns = {"GEOID" : "geoid"})
    tracts["stfips"] = tracts["geoid"].str.slice(0,2)

    print("read in tracts")

    # read through data in chunks of 10K
    iter_csv = pd.read_csv("data/u000.csv", chunksize = 1e4,
                          names = ["advertising_id", "timestamp", "latitude", "longitude", "accuracy"],
                           dtype = {"advertising_id" : str, "timestamp" : int, "latitude" : float,
                            "longitude" : float, "accuracy" : int})
  
  
    # process each chunk of 10K observations
    i = 0
    for dxi, df in enumerate(iter_csv):

        print("chunk ", i)
        
        # drop if the accuracy is too low 
        df.drop(df[df.accuracy == 0].index, inplace = True)

        for st in STATES:

            # get state level tracts
            st_tracts = tracts[tracts.stfips == st]

            # convert lat/lons to Point projected in local plane
            gs = gpd.GeoSeries(index = df.index, crs = fiona.crs.from_epsg(4326), 
                              data = [Point(xy) for xy in zip(df.longitude, df.latitude)])

            # get boundaries for the state 
            state = st_tracts.geometry

            # drop if outside that state's bounding box
            bounds = st_tracts.bounds
            bounds = [bounds.minx.min(), bounds.maxx.max(),bounds.miny.min(), bounds.maxy.max()]
            df.drop(df[~df.apply(cut_box, args = bounds, axis = 1)].index, inplace = True)

            # perform spatial join: point in state polygon 
            gdf = gpd.GeoDataFrame(data = df, geometry = gs)
            gdf.drop(gdf[~gdf.intersects(state)].index, inplace = True)
            gdf.reset_index(inplace = True, drop = True)
            print("joined to state poly")

            # read in OSM ways file
            roads = gpd.read_file("ways/{}_way.geojson".format(st))
            roads = gpd.GeoDataFrame(geometry = roads.buffer(10).to_crs(epsg = 4326))
            roads.index.name = "hway"
            print("read in roads")

            # perform join on major roadways, so we can drop them later.
            gdf["hway"] = 0
            gdf.loc[gpd.sjoin(gdf, roads.copy(), op = "within", how = "inner").index_right, "hway"] = 1
            print("done with roads")

            gdf.advertising_id = gdf.advertising_id.str.lower()

        # # spatial join: remaining lat/lon to tracts, by state
      #     gdf = gpd.sjoin(gdf, tracts[tracts.stfips == s], op = "within", how = "inner")

        # write result to file
        # with open("processed/natl_000_{}.csv".format(dxi)) as f: 

        #   gdf[["advertising_id", "timestamp", "geoid",
        #        "latitude", "longitude", "accuracy", "hway"]]\
        #      .to_csv(f, index = False, float_format='%.5f', header = False)
    
        i += 1
    # return gdf[["advertising_id", "timestamp", "geoid", "latitude", "longitude", "accuracy", "hway", "geometry"]]

import argparse

if __name__ == '__main__': 

  parser = argparse.ArgumentParser()
  parser.add_argument("-n", "--num",  type = int, default = 0, help="A number!")
  parser.add_argument("-c", "--city", type = str, default = "philadelphia", help="City name")
  args = parser.parse_args()

  main(n = args.num)
