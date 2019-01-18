#!/bin/bash

# mkdir places

cd places
for st in 36 06 17 04 48 42 12 39 18 37 53 08 11; do 
   wget https://www2.census.gov/geo/tiger/GENZ2017/shp/cb_2017_${st}_place_500k.zip
   unzip cb_2017_${st}_place_500k.zip
done 

cities="new_york los_angeles chicago houston phoenix philadelphia san_antonio san_diego dallas san_jose austin jacksonville san_francisco columbus fort_worth indianapolis charlotte seattle denver washington"

ogr2ogr -f GeoJSON new_york.geojson      cb_2017_36_place_500k.shp -sql "select * from cb_2017_36_place_500k where NAME = 'New York'" -nln x
ogr2ogr -f GeoJSON los_angeles.geojson   cb_2017_06_place_500k.shp -sql "select * from cb_2017_06_place_500k where NAME = 'Los Angeles'" -nln x
ogr2ogr -f GeoJSON chicago.geojson       cb_2017_17_place_500k.shp -sql "select * from cb_2017_17_place_500k where NAME = 'Chicago'" -nln x
ogr2ogr -f GeoJSON houston.geojson       cb_2017_48_place_500k.shp -sql "select * from cb_2017_48_place_500k where NAME = 'Houston'" -nln x
ogr2ogr -f GeoJSON phoenix.geojson       cb_2017_04_place_500k.shp -sql "select * from cb_2017_04_place_500k where NAME = 'Phoenix'" -nln x
ogr2ogr -f GeoJSON philadelphia.geojson  cb_2017_42_place_500k.shp -sql "select * from cb_2017_42_place_500k where NAME = 'Philadelphia'" -nln x
ogr2ogr -f GeoJSON san_antonio.geojson   cb_2017_48_place_500k.shp -sql "select * from cb_2017_48_place_500k where NAME = 'San Antonio'" -nln x
ogr2ogr -f GeoJSON san_diego.geojson     cb_2017_06_place_500k.shp -sql "select * from cb_2017_06_place_500k where NAME = 'San Diego'" -nln x
ogr2ogr -f GeoJSON dallas.geojson        cb_2017_48_place_500k.shp -sql "select * from cb_2017_48_place_500k where NAME = 'Dallas'" -nln x
ogr2ogr -f GeoJSON san_jose.geojson      cb_2017_06_place_500k.shp -sql "select * from cb_2017_06_place_500k where NAME = 'San Jose'" -nln x
ogr2ogr -f GeoJSON austin.geojson        cb_2017_48_place_500k.shp -sql "select * from cb_2017_48_place_500k where NAME = 'Austin'" -nln x
ogr2ogr -f GeoJSON jacksonville.geojson  cb_2017_12_place_500k.shp -sql "select * from cb_2017_12_place_500k where NAME = 'Jacksonville'" -nln x
ogr2ogr -f GeoJSON san_francisco.geojson cb_2017_06_place_500k.shp -sql "select * from cb_2017_06_place_500k where NAME = 'San Francisco'" -nln x
ogr2ogr -f GeoJSON columbus.geojson      cb_2017_39_place_500k.shp -sql "select * from cb_2017_39_place_500k where NAME = 'Columbus'" -nln x
ogr2ogr -f GeoJSON fort_worth.geojson    cb_2017_48_place_500k.shp -sql "select * from cb_2017_48_place_500k where NAME = 'Fort Worth'" -nln x
ogr2ogr -f GeoJSON indianapolis.geojson  cb_2017_18_place_500k.shp -sql "select * from cb_2017_18_place_500k where NAME = 'Indianapolis city (balance)'" -nln x
ogr2ogr -f GeoJSON charlotte.geojson     cb_2017_37_place_500k.shp -sql "select * from cb_2017_37_place_500k where NAME = 'Charlotte'" -nln x
ogr2ogr -f GeoJSON seattle.geojson       cb_2017_53_place_500k.shp -sql "select * from cb_2017_53_place_500k where NAME = 'Seattle'" -nln x
ogr2ogr -f GeoJSON denver.geojson        cb_2017_08_place_500k.shp -sql "select * from cb_2017_08_place_500k where NAME = 'Denver'" -nln x
ogr2ogr -f GeoJSON washington.geojson    cb_2017_11_place_500k.shp -sql "select * from cb_2017_11_place_500k where NAME = 'Washington'" -nln x

rm *10km.geojson 
for city in $cities; do

  echo ${city}
  cp ${city}.geojson x.geojson
  ogr2ogr -f GeoJSON ${city}_10km.geojson x.geojson -dialect sqlite \
            -sql "select name, ST_Transform(ST_Buffer(ST_Transform(geometry, 2163), 10000), 4326) from x"

  rm x.geojson

done



rm cb_2017*

cd -