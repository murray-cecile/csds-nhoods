#==================================================================#
# PROCESSING - version for whole country
# debugging is forever
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
import pylab
import pytz

STATES = ["11", "10", "01"]

def cut_box(row, *bounds):

  try:
    return bounds[0] < row.longitude < bounds[2] and \
           bounds[1] < row.latitude  < bounds[3]
  except TypeError:
    print(row)
    sys.exit()

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