# Shell script for converting ways.pbf into a shapefile

cd /Users/cecilemurray/CSDS/data

# wget "https://saxon.harris.uchicago.edu/~jsaxon/way.pbf"

ogr2ogr -f "ESRI Shapefile" lines.shp way.pbf -overwrite -dialect sqlite -sql "SELECT osm_id, name, highway, geometry FROM lines" lines

