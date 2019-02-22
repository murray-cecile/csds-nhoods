#===============================================================================#
# PULL COUNTY TIMEZONE ASSOCIATIONS
#
# Cecile Murray
#===============================================================================#

libs <- c("here", "tidyverse", "magrittr", "knitr", "kableExtra", "janitor")
lapply(libs, library, character.only = TRUE)

install.packages("countytimezones")

library(countytimezones)

df <- countytimezones::county_tzs %>% 
  mutate(stcofips = str_pad(as.character(fips), width = 5, side = "left", pad = "0")) %>% 
  select(stcofips, tz)

write_csv(df, "countytimezones.csv")
