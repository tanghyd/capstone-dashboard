import numpy as np
import pandas as pd
import geopandas as gpd
import os

from pipeline.data import report_scores # function to construct report scores

## clearly this is not a database, but the /data folder already exists and i'd like to put functions in /pipeline, stored data in /data, and "in-memory" data shared between pages here ##

# load data from file
events = pd.read_csv(os.path.join('data','event_chunks-d2v_v50-c3-e20-results.csv'), index_col=False) #index_col=0
events['label'] = events['pred'].astype(int)
#events['prob'] = [np.random.uniform(low=0.5,high=1.0) if label else np.random.uniform(low=0.,high=0.499) for label in events['label']]

map_data = pd.read_csv(os.path.join('data','geoview','map_data.zip'), compression='zip', index_col=0, parse_dates=['report_year','date_from','date_to'])
map_data['report_year'] = map_data['report_year'].dt.strftime('%Y')
map_data = map_data.merge(report_scores(events, by_anumber=True), on='anumber')
map_data.score = map_data.score.round(4)

map_geometry = gpd.read_file(os.path.join('zip://','data', 'geoview', 'map_geometry.zip'), index_col=0)
