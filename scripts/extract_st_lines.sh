
# 01 02
stlist="04 05 06 08 09 10 11 12 13 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 44 45 46 47 48 49 50 51 53 54 55 56"

for st in $stlist; do

    echo $st

    ogr2ogr -f GeoJSON states/${st}_tracts.geojson states/${st}_tracts.shp
    osmium extract -f osm -p states/${st}_tracts.geojson ways/way.pbf  -o way.pbf --overwrite
    ogr2ogr -f GeoJSON ways/${st}_way.geojson way.pbf lines

done

