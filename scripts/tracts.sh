cd tracts

# wget ftp://ftp2.census.gov/geo/tiger/GENZ2015/shp/cb_2015_*_tract_500k.zip

for x in *zip; do unzip $x; done

rm us_tracts.*
for i in $(ls cb*.shp); do

  if [ -f "us_tracts.shp" ]; then
    ogr2ogr -update -append us_tracts.shp $i -nln us_tracts
  else
    ogr2ogr us_tracts.shp $i
	    fi
done

rm cb_*

# cities="new_york los_angeles chicago houston phoenix philadelphia san_antonio san_diego dallas san_jose austin jacksonville san_francisco columbus fort_worth indianapolis charlotte seattle denver washington"

# for city in $cities; do

#   ogr2ogr -clipsrc ../places/${city}_10km.geojson -f GeoJSON ${city}.geojson us_tracts.shp

# done

cd -