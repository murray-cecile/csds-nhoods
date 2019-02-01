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

def cut_box(row, x1, y1, x2, y2):

  try:
    return x1 < row.longitude < x2 and \
           y1 < row.latitude  < y2
  except TypeError:
    print(row)
    sys.exit()

def main(n = 0):

    # read in tract file
    tracts = gpd.read_file("tracts/us_tracts.shp")
    tracts = tracts[["GEOID", "geometry"]].rename(columns = {"GEOID" : "geoid"})

    # read in OSM ways file
    roads = gpd.read_file("ways/lines.shp")
    roads = gpd.GeoDataFrame(geometry = roads.buffer(10).to_crs(epsg = 4326))
    roads.index.name = "hway"


    # read through data in chunks of 1M
    iter_csv = pd.read_csv("data/u000.csv", chunksize = 1e3,
                          names = ["advertising_id", "timestamp", "latitude", "longitude", "accuracy"],
                           dtype = {"advertising_id" : str, "timestamp" : int, "latitude" : float,
                            "longitude" : float, "accuracy" : int})

    # process each chunk of 1M observations
    for dxi, df in enumerate(iter_csv):

        print("chunk", dxi, flush = True)

        # drop if the accuracy is too low or if the point is not inside city bounding lat/lon
        df.drop(df[df.accuracy == 0].index, inplace = True)

        # convert lat/lons to Point projected in local plane
        gs = gpd.GeoSeries(index = df.index, crs = fiona.crs.from_epsg(4326), 
                           data = [Point(xy) for xy in zip(df.longitude, df.latitude)])

        # perform join on major roadways, so we can drop them later.
        gdf["hway"] = 0
        gdf.loc[gpd.sjoin(gdf, roads.copy(), op = "within", how = "inner").index, "hway"] = 1

        # spatial join: remaining lat/lon to tracts
        gdf = gpd.sjoin(gdf, tracts, op = "within", how = "inner")

        gdf.advertising_id = gdf.advertising_id.str.lower()

        # write result to file
        with open("processed/natl_{:03d}.csv".format(n), 'a') as f: 

          gdf[["advertising_id", "timestamp", "geoid",
               "latitude", "longitude", "accuracy", "hway"]]\
             .to_csv(f, index = False, float_format='%.5f', header = False)
    
    # return gdf[["advertising_id", "timestamp", "geoid", "latitude", "longitude", "accuracy", "hway", "geometry"]]

import argparse

if __name__ == '__main__': 

  parser = argparse.ArgumentParser()
  parser.add_argument("-n", "--num",  type = int, default = 0, help="A number!")
  parser.add_argument("-c", "--city", type = str, default = "philadelphia", help="City name")
  args = parser.parse_args()

  main(n = args.num)
