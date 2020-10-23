import numpy as np
import pandas as pd
import geopandas as gpd
import os 

# load data
events = pd.read_csv(os.path.join('data','events_high-conf.csv'), index_col=0)
events['label'] = events['label'].astype(int)

commodities = pd.read_csv(os.path.join('data','commodities_high-conf.csv'),index_col=0)

capstone_files = pd.read_csv(os.path.join('data','capstone_files.zip'), compression='zip')

# load geoview metadata and shape files
metadata = pd.read_csv(os.path.join('data','geoview','capstone_metadata.zip'), compression='zip', parse_dates=['report_year'],
    usecols=['anumber','title','report_type','project','keywords','commodity','report_year'])

geoview = gpd.read_file(os.path.join('zip://','data', 'geoview', 'capstone_shapefiles.shp.zip'))

# build geopandas.geodataframe.GeoDataFrame (to start with geoview to preserve data type for plotly map)
# join geoview shape files, geoview metadata, capstone json to anumber mapping, and aggregated event statistics
map_data = geoview.merge(metadata, on='anumber').merge(capstone_files, on='anumber').merge(
    events.groupby('filename')['label'].sum().reset_index(), on='filename')
map_data['epoch'] = map_data.report_year.astype(np.int64).divide(1e9).astype(np.int64)