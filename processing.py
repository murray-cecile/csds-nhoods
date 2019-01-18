#==================================================================#
# PROCESSING - copy from jsaxon/parks
# Cecile Murray
#==================================================================#

import geopandas as gpd
import pandas    as pd
import numpy     as np

from shapely.geometry import Point

from fiona.crs import from_epsg

import os
import csv

import sys


cities = ["new_york", "los_angeles", "chicago", "houston", "phoenix", 
          "philadelphia", "san_antonio", "san_diego", "dallas", "san_jose", 
          "austin", "jacksonville", "san_francisco", "columbus", "fort_worth", 
          "indianapolis", "charlotte", "seattle", "denver", "washington"]

cities = ["philadelphia"]

epsg   = {"new_york" : 3623, "los_angeles" : 3488, "chicago" : 3528, "houston" : 3665, "phoenix" : 3478, 
          "philadelphia" : 3364, "san_antonio" : 3665, "san_diego" : 3488, "dallas" : 3665, "san_jose" : 3488, 
          "austin" : 3665, "jacksonville" : 3513, "san_francisco" : 3488, "columbus" : 3637, "fort_worth" : 3665, 
          "indianapolis" : 3532, "charlotte" : 3631, "seattle" : 3689, "denver" : 3501, "washington" : 3689}


def ens_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(file_path)
        
# for c in cities:
#     ens_dir("processed/" + c + "/")