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

DATADIR = "data/"
TRACTDIR = "tracts/"
WAYSDIR = "ways/"
PROCESSED = "processed/"

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
  
    r = gpd.read_file(WAYSDIR + '{}_way.geojson'.format(st))

    r.index.name = "hway"
    r = r.drop(['z_order', 'other_tags'], axis = 1)

    r = gpd.GeoDataFrame(geometry = r.geometry.to_crs(epsg = 4326).buffer(10)) 
    # print(r.head())
    # print("road projection is " + str(r.crs))

    return r

def get_st_tracts(st):
    ''' reads in US tract shapefile and returns state-specific geodataframe'''

    tracts = gpd.read_file(TRACTDIR + "us_tracts.shp")
    tracts = tracts[["GEOID", "geometry"]].rename(columns = {"GEOID" : "geoid"})
    tracts["stfips"] = tracts["geoid"].str.slice(0,2)
    st_tracts = tracts[tracts["stfips"] == st]
    
    return st_tracts.to_crs(epsg = 4326) # note: file comes in 4269


def main(j, st):

    st_tracts = get_st_tracts(st)
    print("tract projection is ", st_tracts.crs)

    roads = read_roads(st)

    iter_csv = pd.read_csv(DATADIR + 'u{:02d}0.csv'.format(j), chunksize = 1e5, 
                           names = ["advertising_id", "timestamp", "latitude", "longitude", "accuracy"])

    for dxi, df in enumerate(iter_csv):

        print("processing chunk #" + str(dxi))
        print("df dimensions are: ", df.shape)

        # drop inaccurate observations
        df.drop(df[df.accuracy == 0].index, inplace = True)
        print("df dimensions are: ", df.shape)

        # convert lat/lons to Point 
        gs = gpd.GeoSeries(index = df.index, crs = fiona.crs.from_epsg(4326), 
                    data = [Point(xy) for xy in zip(df.longitude, df.latitude)]).to_crs(epsg = 4326)
        gdf = gpd.GeoDataFrame(data = df, geometry = gs)
        print("gdf projection is " + str(gdf.crs))
        print(gdf.head())


        # drop observations outside the state
        state_blob = st_tracts.dissolve(by='stfips')
        # print(state_blob.head())
        bounds = state_blob.bounds
        # print("state blob bounds:" + str(bounds))
        # print("state tracts are in crs: " + str(state_blob.crs))
        bounds = [bounds.minx.min(), bounds.maxx.max(),bounds.miny.min(), bounds.maxy.max()]
        gdf.drop(df[~gdf.apply(cut_box, args = bounds, axis = 1)].index, inplace = True)
        gdf.reset_index(inplace = True, drop = True)


        gdf.advertising_id = gdf.advertising_id.str.lower()

        print(gdf.shape)
        print(st_tracts.shape)
        print(st_tracts.head())


        # project state tract file and join remaining points to tracts
        try:
            gdf = gpd.sjoin(gdf, st_tracts, op = "within", how = "inner")
            gdf.set_index(keys = 'index_right', inplace = True, drop = True)
            print("gdf.index: ", gdf.index)

        except(AttributeError):
            print("no observations in this state?")
            continue

        # perform join on major roadways, so we can drop them later
        gdf["hway"] = 0
        try:
            gdf.loc[gpd.sjoin(gdf,roads.copy(), op = "within", how = "inner").index, "hway"] = 1
        
        except(AttributeError):
            print("no observations on roads?")
        
        finally:

            with open(PROCESSED + 'pr_{:02d}_{}.csv'.format(j, st), "a") as f: 

                gdf[["advertising_id", "timestamp", "geoid",
                "latitude", "longitude", "accuracy", "hway"]].to_csv(f, index = False, float_format='%.5f', header = False)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-j", "--num",  type = int, default = 0, help="A number!")
    parser.add_argument("-st", "--state", type = str, default = "11", help="State FIPS code")
    args = parser.parse_args()

    main(j = args.num, st = args.state)
