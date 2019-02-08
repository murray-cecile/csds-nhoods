#!/bin/bash

# mkdir states
cd states/

# get the shapefiles, unzip, and separate
# wget https://www2.census.gov/geo/tiger/GENZ2017/shp/cb_2017_us_state_500k.zip
# unzip cb_2017_us_state_500k.zip
# python cut_states.py

stlist="01 02 04 05 06 08 09 10 11 12 13 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 44 45 46 47 48 49 50 51 53 54 55 56"

for st in $stlist; do 

   echo $st
   ogr2ogr -f GeoJSON ${st}_state.geojson ${st}_state.shp 

done

ext="cpg dbf prj shp shx"

for st in $stlist; do
   for e in $ext; do
      rm ${st}_state.${e}
   done
done

cd -
