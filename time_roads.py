#==================================================================#
# TIME ROADS OPERATIONS
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
import time

# STATES = ["01", "02", "04", "05", "06", "08", "09", "10", "11", "12", "13",
#  "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27",
#   "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40",
#   "41", "42", "44", "45", "46", "47", "48", "49", "50", "51", "53", "54", "55", "56"]

STATES = ["01", "02", "04", "05", "06"]

if __name__ == "__main__":
    
    road_dict = {}

    for st in STATES:
        start = time.time()
        r = gpd.read_file('ways/{}_way.geojson'.format(st))
        print("file read for state " + st + ": " + str(time.time() - start))
        read_time = time.time()
        r.index.name = "hway"
        r = gpd.GeoDataFrame(geometry = r.geometry.to_crs(epsg = 2163).buffer(10)) 
        buffer_time = time.time()
        print("buffer for state " + st + ": " + str(buffer_time - read_time))
        road_dict[st] = r
        # r = None