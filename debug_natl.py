#==================================================================#
# PROCESSING - version for whole country
# debugging is forever
# Cecile Murray
#==================================================================#

import geopandas as gpd
import pandas    as pd
import numpy     as np
import matplotlib as plt

from shapely.geometry import Point
import fiona.crs # from fiona.crs import from_espg raised an error

import os
import csv
import sys

# STATES = ["01", "02", "04", "05", "06", "08", "09", "10", "11", "12", "13",
#  "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27",
#   "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40",
#   "41", "42", "44", "45", "46", "47", "48", "49", "50", "51", "53", "54", "55", "56"]


STATES = ["11", "10", "04"]

def cut_box(row, *bounds):

  try:
    return bounds[0] < row.longitude < bounds[2] and \
           bounds[1] < row.latitude  < bounds[3]
  except TypeError:
    print(row)
    sys.exit()

def read_roads(state_list = STATES):
  
  road_dict = {}

  for st in state_list:

        start = time.time()

        r = gpd.read_file('ways/{}_way.geojson'.format(st))
        print("file read for state " + st + ": " + str(time.time() - start))
        read_time = time.time()

        r.index.name = "hway"
        r.drop(['z_order', 'other_tags'], axis = 1)

        r = gpd.GeoDataFrame(geometry = r.geometry.to_crs(epsg = 2163).buffer(10)) 
        buffer_time = time.time()
        print("buffer for state " + st + ": " + str(buffer_time - read_time))
        
        road_dict[st] = r

  return road_dict

if __name__ == "__main__":
    
    # read in tract file
    tracts = gpd.read_file("tracts/us_tracts.shp").to_crs(epsg = 4326)
    tracts = tracts[["GEOID", "geometry"]].rename(columns = {"GEOID" : "geoid"})
    tracts["stfips"] = tracts["geoid"].str.slice(0,2)

    df = pd.read_csv("data/u000.csv", nrows = 1e5, names = ["advertising_id", "timestamp", "latitude", "longitude", "accuracy"])
    df.drop(df[df.accuracy == 0].index, inplace = True)
    print(df.shape)


    

    for st in STATES:

      # get state level tracts
      st_tracts = tracts[tracts.stfips == st]
      print(st_tracts.shape)

      # get boundaries for the state 
      # state = st_tracts.geometry

      # drop if outside that state's bounding box
      bounds = st_tracts.bounds
      bounds = [bounds.minx.min(), bounds.maxx.max(),bounds.miny.min(), bounds.maxy.max()]
      df.drop(df[~df.apply(cut_box, args = bounds, axis = 1)].index, inplace = True)
      print(df.shape)

      # convert lat/lons to Point 
      gs = gpd.GeoSeries(index = df.index, crs = fiona.crs.from_epsg(4326), 
                          data = [Point(xy) for xy in zip(df.longitude, df.latitude)]).to_crs(epsg = 2163)
      

      # # perform spatial join: point in state polygon 
      gdf = gpd.GeoDataFrame(data = df, geometry = gs)
      # gdf.drop(gdf[~gdf.intersects(state)].index, inplace = True)
      gdf.reset_index(inplace = True, drop = True)
      # print("joined to state poly")
      print(gdf.shape)

      # read in OSM ways file
      roads = gpd.read_file("ways/{}_way.geojson".format(st))
      print("read in roads")

      roads.index.name = "hway"
      roads = gpd.GeoDataFrame(geometry = roads.geometry.to_crs(epsg = 2163).buffer(10))
      print("buffered roads")

      # perform join on major roadways, so we can drop them later.
      gdf["hway"] = 0
      gdf.loc[gpd.sjoin(gdf,roads.copy(), op = "within", how = "inner").index, "hway"] = 1
      print("joined with roads")

      gdf.advertising_id = gdf.advertising_id.str.lower()

      st_tracts = st_tracts.to_crs(epsg=2163) #gpd.GeoDataFrame(geometry = st_tracts.geometry.to_crs(2163))
      gdf2 = gpd.sjoin(gdf, st_tracts, op = "within", how = "inner")
      print("done with " + st)