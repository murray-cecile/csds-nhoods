#==================================================================#
# EXTRACT STATE-LEVEL SHAPEFILES
# Cecile Murray
#==================================================================#

import geopandas as gpd
import pandas    as pd
import numpy     as np

from shapely.geometry import Point
import fiona.crs 

import os
import csv
import sys


STATES = ["01", "02", "04", "05", "06", "08", "09", "10", "11", "12", "13", "15",
          "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", 
          "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", 
          "42", "44", "45", "46", "47", "48", "49", "50", "51", "53", "54", "55", "56"] 

def cut_box(row, x1, y1, x2, y2):

  try:
    return x1 < row.longitude < x2 and \
           y1 < row.latitude  < y2
  except TypeError:
    print(row)
    sys.exit()

def main(*stlist):

    if not stlist:
        stlist = STATES

    # read in tract file
    tracts = gpd.read_file(filename="tracts/us_tracts.shp")
    tracts = tracts[["GEOID", "geometry"]].rename(columns = {"GEOID" : "geoid"})
    tracts["stfips"] = tracts["geoid"].str.slice(0,2)

    for st in stlist:
        print("processing " + st)
        st_tracts = tracts[tracts.stfips == st]
        st_tracts.to_file(filename='states/{}_tracts.shp'.format(st))

if __name__ == "__main__":
    
    main()