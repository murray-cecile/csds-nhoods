#==================================================================#
# DEBUG ROAD BUFFER
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
import matplotlib.pyplot as plt

if __name__ == "__main__":
    
    # read in OSM ways file
    st = "11"
    roads = gpd.read_file("ways/{}_way.geojson".format(st))
    print("read in roads")

    buffer = gpd.GeoDataFrame(geometry = roads.geometry.to_crs(epsg = 2136)).buffer(10) 

    road_plot = roads.plot()

    roads.index.name = "hway"
    
    dc_tracts = gpd.read_file("tracts/washington.geojson")
    dcplot = dc_tracts.plot()
