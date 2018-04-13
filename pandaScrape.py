import pandas as pd

hdata = pd.read_csv('https://rotogrinders.com/projected-stats/mlb-hitter.csv?site=draftkings', index_col=0)

hdata.to_csv('hitterprojections.csv')

pdata = pd.read_csv('https://rotogrinders.com/projected-stats/mlb-pitcher.csv?site=draftkings', index_col=0)

pdata.to_csv('pitcherprojections.csv')