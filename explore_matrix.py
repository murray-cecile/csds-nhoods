#==================================================================#
# MAKE GRAPH MATRICES
# computes neighborhood relationships based on state processed data
#
# Cecile Murray
#==================================================================#

import pandas as pd

df = pd.read_csv('processed/states/all_11_visits.csv.bz2')

homes = df.loc[df.home==True].groupby(['tract']).sum().reset_index()
homes.columns = ['home', 'visits', 'nusers']

visits = df[['uid', 'visits']].groupby(['uid']).sum()
users = df.loc[df.home==True]
users.columns = ['uid', 'home', 'visits', 'is_home']

master = pd.merge(df, visits, how='inner', on='uid', suffixes=('_here', '_tot'))
master['frac_here'] = master['visits_here'] / master['visits_tot']
master['home'] = master['home'] * master['tract']
master = pd.merge(master, users[['uid', 'home']], how='left', on='uid')

wts = master.groupby(['tract', 'home_y']).sum().reset_index()
wts.columns = ['tract', 'home', 'visits_here', 'is_home', 'visits_tot', 'frac_here']
# this is wrong
# master_sum.drop(master_sum[master_sum.home == 0].index, inplace=True)

wts = pd.merge(wts, homes[['home', 'nusers']], how='left', on='home')
wts['wt'] = wts['frac_here'] / wts['nusers']

wts.drop(wts[wts.tract==wts.home].index, inplace=True)
wts.sort_values(by=['wt'])
wts.home = wts.home.astype('int64')