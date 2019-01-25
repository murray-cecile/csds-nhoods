wget http://download.geofabrik.de/north-america-latest.osm.pbf -O /tmp/north-america-latest.osm.pbf

osmium tags-filter -o /tmp/way.pbf    /tmp/north-america-latest.osm.pbf -e way.extract


for city in $cities; do

    echo $city

    osmium extract -f osm -p places/${city}_10km.geojson /tmp/way.pbf  -o way.pbf --overwrite
    ogr2ogr -f GeoJSON ${city}_way.geojson way.pbf lines

done

mkdir ways
mv *.geojson ways/