#==================================================================#
# PERFORM NATIONAL JOIN FOR ENTIRE COUNTRY
# time performance for load balancing
#
# Cecile Murray
#==================================================================#

import geopandas as gpd
import pandas    as pd
import numpy     as np
import matplotlib as plt

from shapely.geometry import Point
import fiona.crs 

import os
import csv
import sys
import time

STATES = ["01", "04", "05", "06", "08"] #, "02", "09", "10", "11", "12", "13",
#  "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27",
#   "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40",
#   "41", "42", "44", "45", "46", "47", "48", "49", "50", "51", "53", "54", "55", "56"]



def cut_box(row, *bounds):

  try:
    return bounds[0] < row.longitude < bounds[2] and \
           bounds[1] < row.latitude  < bounds[3]
  except TypeError:
    print(row)
    sys.exit()

def track_time(description, start):
    ''' Takes a descriptive string and a start time,
     prints how long it's been since start, returns current time'''

    now = time.time()
    print(description + str(round(now - start, 2)))
    return now

def read_roads(state_list = STATES):
  ''' Takes list of state FIPS codes, reads in ways file, buffers it, returns dict of all'''
  
  road_dict = {}

  for st in state_list:

        start = time.time()
        print("start time is: " + start)

        r = gpd.read_file('ways/{}_way.geojson'.format(st))
        read_time = track_time('file read for state {}: '.format(st), start)
        read_time = time.time()

        r.index.name = "hway"
        r.drop(['z_order', 'other_tags'], axis = 1)

        r = gpd.GeoDataFrame(geometry = r.geometry.to_crs(epsg = 2163).buffer(10)) 
        buffer_time = track_time('buffer for state {}: '.format(st), read_time)
        
        road_dict[st] = r

  return road_dict


if __name__ == "__main__":
    
    start = time.time()

    # read in tract file
    tracts = gpd.read_file("tracts/us_tracts.shp").to_crs(epsg = 4326)
    tracts = tracts[["GEOID", "geometry"]].rename(columns = {"GEOID" : "geoid"})
    tracts["stfips"] = tracts["geoid"].str.slice(0,2)
    t_time = track_time("tract shapefile is read in: ", start)

    df = pd.read_csv("data/u000.csv", nrows = 1e5, names = ["advertising_id", "timestamp", "latitude", "longitude", "accuracy"])
    df.drop(df[df.accuracy == 0].index, inplace = True)
    d_time = track_time("data are read in & inaccurate obvs dropped: ", t_time)

    road_dict = read_roads(STATES)
    r_time  = track_time("roads read in and buffered: ", d_time)
    
    final_time = 0
    for st in STATES:

        loop_time = time.time()
        print("starting state " + st)

        # get state level tracts
        st_tracts = tracts[tracts.stfips == st]

        # drop if outside that state's bounding box
        bounds = st_tracts.bounds
        bounds = [bounds.minx.min(), bounds.maxx.max(),bounds.miny.min(), bounds.maxy.max()]
        df.drop(df[~df.apply(cut_box, args = bounds, axis = 1)].index, inplace = True)

        # convert lat/lons to Point 
        gs = gpd.GeoSeries(index = df.index, crs = fiona.crs.from_epsg(4326), 
                            data = [Point(xy) for xy in zip(df.longitude, df.latitude)]).to_crs(epsg = 2163)
        gdf = gpd.GeoDataFrame(data = df, geometry = gs)
        gdf.reset_index(inplace = True, drop = True)


        # perform join on major roadways, so we can drop them later.
        try:
            gdf["hway"] = 0
            gdf.loc[gpd.sjoin(gdf,road_dict[st].copy(), op = "within", how = "inner").index, "hway"] = 1
            rjoin_time = track_time("road buffer join complete ", loop_time)
        
        except(AttributeError):
            print("probably hit that r tree error about no observations, skipping the join")
            continue


        gdf.advertising_id = gdf.advertising_id.str.lower()

        st_tracts = st_tracts.to_crs(epsg=2163) #gpd.GeoDataFrame(geometry = st_tracts.geometry.to_crs(2163))
        gdf = gpd.sjoin(gdf, st_tracts, op = "within", how = "inner")
        trjoin_time = track_time("tract polygon join complete ", rjoin_time)

        with open("processed/natl_000.csv", "a") as f: 

            gdf[["advertising_id", "timestamp", "geoid",
               "latitude", "longitude", "accuracy", "hway"]].to_csv(f, index = False, float_format='%.5f', header = False)
        
        final_time = time.time()
        print("\n")
    
    end = track_time("final time total: ", start)