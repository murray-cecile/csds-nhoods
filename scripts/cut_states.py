#==================================================================#
# CUT UP FULL STATE SHAPEFILES
# Cecile Murray
#==================================================================#

import geopandas as gpd
import fiona

STATES = ["01", "02", "04", "05", "06", "08", "09", "10", "11", "12", "13",
 "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27",
  "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40",
  "41", "42", "44", "45", "46", "47", "48", "49", "50", "51", "53", "54", "55", "56"]

def main():

    all_st = gpd.read_file("states/cb_2017_us_state_500k.shp")
    all_st = all_st[["GEOID", "geometry"]].rename(columns = {"GEOID" : "geoid"})

    for st in STATES:

        print("processing " + st)
        state = all_st[all_st.geoid.str.slice(0,2) == st]
        state.to_file("states/{}_state.shp".format(st))

if __name__ == "__main__":
    main()