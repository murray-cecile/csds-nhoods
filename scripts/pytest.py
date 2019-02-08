#!/usr/bin/env python 

import pandas as pd
import geopandas as gpd 

l = pd.DataFrame([i for i in range(0,10)])
l.to_csv("pytest.csv")
