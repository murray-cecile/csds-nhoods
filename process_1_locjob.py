#==================================================================#
# PROCESS ONE JOB
# Perform spatial join for one file-state combination (single job)
#
# Cecile Murray
#==================================================================#

import geopandas as gpd
import pandas    as pd
import numpy     as np

from shapely.geometry import Point
import fiona.crs 
from rtree.core import RTreeError

import os
import csv
import sys
import argparse
import time

# working directory is /home/cmmurray/stash

DATADIR = "data/"
TRACTDIR = "tracts/"
WAYSDIR = "ways/"
PROCESSED = "processed/"

OUT_VARS = ["advertising_id", "timestamp", "geoid", "latitude", "longitude", "accuracy", "hway"]

def cut_box(row, *bounds):
    ''' checks whether a point falls inside coords of a bounding box '''

    try:
        return bounds[0] < row.longitude < bounds[2] and \
            bounds[1] < row.latitude  < bounds[3]
    except TypeError:
        print(row)
        sys.exit()

def read_roads(st):
    ''' Reads in ways file and buffers it, returns projected GeoDataFrame'''
  
    r = gpd.read_file(WAYSDIR + '{}_way.geojson'.format(st)) #comes in 4326

    r.index.name = "hway"
    r = r.drop(['z_order', 'other_tags'], axis = 1)

    r = gpd.GeoDataFrame(geometry = r.geometry.to_crs(epsg = 2163).buffer(10)).to_crs(epsg = 4326)
    # print(r.head())
    # print("road projection is " + str(r.crs))

    return r

def get_st_tracts(st):
    ''' reads in US tract shapefile and returns state-specific geodataframe'''

    tracts = gpd.read_file(TRACTDIR + "us_tracts.geojson")
    tracts = tracts[["GEOID", "geometry"]].rename(columns = {"GEOID" : "geoid"})
    tracts["stfips"] = tracts["geoid"].str.slice(0,2)
    st_tracts = tracts[tracts["stfips"] == st]
    
    return st_tracts.to_crs(epsg = 4326) # note: file comes in 4269


def main(j, st):

    start = time.time()

    print('processing state {} in user id group {:02d}'.format(st, j))

    st_tracts = get_st_tracts(st)
    # print("tract projection is ", st_tracts.crs)

    state_blob = st_tracts.dissolve(by='stfips')
    # print(state_blob.head())
    bounds = state_blob.bounds
    print("state blob bounds:" + str(bounds))
    bounds = [bounds.minx.min(), bounds.maxx.max(),bounds.miny.min(), bounds.maxy.max()]

    roads = read_roads(st)

    print(time.time() - start)

    iter_csv = pd.read_csv(DATADIR + 'u000-2.csv', chunksize = 1e5, 
                           names = ["advertising_id", "timestamp", "latitude", "longitude", "accuracy"])

    for dxi, df in enumerate(iter_csv):

        print("processing chunk #" + str(dxi), flush=True, end = " ")
        # print("df dimensions are: ", df.shape)

        # if dxi < 1:
        #     continue
        if dxi == 10:
            break

        df['row'] = df.index

        # drop inaccurate observations
        df.drop(df[df.accuracy == 0].index, inplace = True)
        # print("df dimensions are: ", df.shape)

        # suprising: case of empty df because all observations have low accuracy?
        if df.empty:
            continue

        # drop observations outside the state
        # print("state tracts are in crs: " + str(state_blob.crs))
        df.drop(df[~df.apply(cut_box, args = bounds, axis = 1)].index, inplace = True)
        df.reset_index(inplace = True, drop = True)

        if df.empty:
            continue
        print("after applying state bbox: ", df.shape)

        # df['advertising_id'] = df.advertising_id.str.lower()


        # convert lat/lons to Point 
        gs = gpd.GeoSeries(index = df.index, crs = fiona.crs.from_epsg(4326), 
                    data = [Point(xy) for xy in zip(df.longitude, df.latitude)])
        gdf = gpd.GeoDataFrame(data = df, geometry = gs)
        # print("gdf projection is " + str(gdf.crs))
        print(gdf.head())

        print('st_tracts.shape:', st_tracts.shape)
        # print(st_tracts.head())

        if df.empty:
            continue

        # project state tract file and join remaining points to tracts
        try:
            print("starting tract spatial join")
            gdf = gpd.sjoin(gdf, st_tracts, op = "within", how = "inner")
            gdf.set_index(keys = 'index_right', inplace = True, drop = True)
            # print("gdf.index: ", gdf.index)

        except(AttributeError):
            print("no observations in this state?")
            continue

        # perform join on major roadways, so we can drop them later
        gdf["hway"] = 0
        try:
            print("starting ways spatial join")
            gdf.loc[gpd.sjoin(gdf,roads.copy(), op = "within", how = "inner").index, "hway"] = 1
        
        except(AttributeError):
            print("no observations on roads?")
        
        finally:

            print("writing to file")

            gdf[OUT_VARS].to_csv(PROCESSED + 'u_{:02d}_{}.csv.bz2'.format(j, st),
                                mode = "a", compression = 'bz2', index = False, float_format='%.5f', header = False)


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-j", "--num",  type = int, default = 0, help="A number!")
    parser.add_argument("-st", "--state", type = str, default = "11", help="State FIPS code")
    args = parser.parse_args()

    main(j = args.num, st = args.state)
