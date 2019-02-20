#==================================================================#
# PROCESSING - copy from jsaxon/parks
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


cities = ["new_york", "los_angeles", "chicago", "houston", "phoenix", 
          "philadelphia", "san_antonio", "san_diego", "dallas", "san_jose", 
          "austin", "jacksonville", "san_francisco", "columbus", "fort_worth", 
          "indianapolis", "charlotte", "seattle", "denver", "washington"]

# cities = ["philadelphia"]

epsg   = {"new_york" : 3623, "los_angeles" : 3488, "chicago" : 3528, "houston" : 3665, "phoenix" : 3478, 
          "philadelphia" : 3364, "san_antonio" : 3665, "san_diego" : 3488, "dallas" : 3665, "san_jose" : 3488, 
          "austin" : 3665, "jacksonville" : 3513, "san_francisco" : 3488, "columbus" : 3637, "fort_worth" : 3665, 
          "indianapolis" : 3532, "charlotte" : 3631, "seattle" : 3689, "denver" : 3501, "washington" : 3689}


def ens_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(file_path)
        
for c in cities:
    ens_dir("processed/" + c + "/")

def cut_box(row, x1, y1, x2, y2):

  try:
    return x1 < row.longitude < x2 and \
           y1 < row.latitude  < y2
  except TypeError:
    print(row)
    sys.exit()

def main(n = 0, c = "philadelphia"):

    if n in [58, 403]: return

    print("Now processing {}, job {}.".format(c, n))

    # read in city-level geojson file
    pl = gpd.read_file("places/{}_10km.geojson".format(c)).to_crs(epsg = 4326)
    places = pl.ix[0].geometry
    bounds = places.bounds

    # read in tract file
    tracts = gpd.read_file("tracts/{}.geojson".format(c)).to_crs(epsg = 4326)
    tracts = tracts[["GEOID", "geometry"]].rename(columns = {"GEOID" : "geoid"})

    # read in OSM ways file
    roads = gpd.read_file("ways/{}_way.geojson".format(c))
    roads = gpd.GeoDataFrame(geometry = roads.buffer(10).to_crs(epsg = 4326))
    roads.index.name = "hway"


    with open("processed/{}_{:03d}.csv".format(c, n), 'w') as f: pass

    # read through data in chunks of 1M
    iter_csv = pd.read_csv("data/u000-2.csv", chunksize = 1e6,
                          names = ["advertising_id", "timestamp", "latitude", "longitude", "accuracy"],
                           dtype = {"advertising_id" : str, "timestamp" : int, "latitude" : float,
                            "longitude" : float, "accuracy" : int})

    # process each chunk of 1M observations
    for dxi, df in enumerate(iter_csv):

        print("chunk", dxi, flush = True)

        # drop if the accuracy is too low or if the point is not inside city bounding lat/lon
        df.drop(df[df.accuracy == 0].index, inplace = True)
        df.drop(df[~df.apply(cut_box, args = bounds, axis = 1)].index, inplace = True)

        # convert lat/lons to Point projected in local plane
        gs = gpd.GeoSeries(index = df.index, crs = fiona.crs.from_epsg(4326), 
                           data = [Point(xy) for xy in zip(df.longitude, df.latitude)])

        # perform spatial join: point in place polygon
        gdf = gpd.GeoDataFrame(data = df, geometry = gs)
        gdf.drop(gdf[~gdf.intersects(places)].index, inplace = True)
        gdf.reset_index(inplace = True, drop = True)

        # perform join on major roadways, so we can drop them later.
        gdf["hway"] = 0
        gdf.loc[gpd.sjoin(gdf, roads.copy(), op = "within", how = "inner").index, "hway"] = 1

        # spatial join: remaining lat/lon to tracts
        gdf = gpd.sjoin(gdf, tracts, op = "within", how = "inner")

        gdf.advertising_id = gdf.advertising_id.str.lower()

        # write result to file
        with open("processed/{}_{:03d}.csv".format(c, n), 'a') as f: 

          gdf[["advertising_id", "timestamp", "geoid",
               "latitude", "longitude", "accuracy", "hway"]]\
             .to_csv(f, index = False, float_format='%.5f', header = False)
    
    # return gdf[["advertising_id", "timestamp", "geoid", "latitude", "longitude", "accuracy", "hway", "geometry"]]


# import multiprocessing


# def run_city_dict(d): main(**d)

# def queue_cities():

#   arg_list = []
#   for c in cities:
#     for n in range(500):
#       arg_list.append({"n" : n, "c" : c})

#   p = multiprocessing.Pool(12)
#   p.map(run_city_dict, arg_list)



# with open("processing.out", "w") as out: pass

# main(n = 0, city = "philadelphia")

import argparse

if __name__ == '__main__': 

  parser = argparse.ArgumentParser()
  parser.add_argument("-n", "--num",  type = int, default = 0, help="A number!")
  parser.add_argument("-c", "--city", type = str, default = "philadelphia", help="City name")
  args = parser.parse_args()

  main(n = args.num, c = args.city)
