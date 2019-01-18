wget http://download.geofabrik.de/north-america-latest.osm.pbf -O /tmp/north-america-latest.osm.pbf

# LD_LIBRARY_PATH=/Users/cecilemurray/anaconda3/lib 
     osmium tags-filter -o /tmp/way.pbf    /tmp/north-america-latest.osm.pbf -e way.extract



