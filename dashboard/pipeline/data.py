import numpy as np
import pandas as pd
import geopandas as gpd
import os 

def group_event_score(events, by_anumber=True, index=False):
    '''Takes the events dataframe as input with filename and anumber in columns.
    Groups by filename or a_number to produce a report score given each identified event computed by
    product sum of (1 - P'(X)), a score analogous to the likelihood of at least one event assuming indepence
    '''
    # whether to group by filename or anumber
    if by_anumber:  # Calculate 1 - P'(X) for each anumber
        df = events.groupby('anumber').prob.apply(
            lambda x : x.subtract(1).multiply(-1).prod()
        ).fillna(1).multiply(-1).add(1)
                            
    # group by filename - Calculate 1 - P'(X) for each filename
    else:
        df = events.groupby(['anumber','filename']).prob.apply(
            lambda x : x.subtract(1).multiply(-1).prod()
        ).fillna(1).multiply(-1).add(1)
    
    # rename prob of each event to score for report
    df.name = 'score'
        
    # reset index after groupby
    if index:
        return df
    return df.reset_index()

# load data
events = pd.read_csv(os.path.join('data','events_high-conf.csv'), index_col=0)
events['label'] = events['label'].astype(int)
events['prob'] = [np.random.uniform(low=0.5,high=1.0) if label else np.random.uniform(low=0.,high=0.499) for label in events['label']]

#commodities = pd.read_csv(os.path.join('data','commodities_high-conf.csv'),index_col=0)

capstone_files = pd.read_csv(os.path.join('data','capstone_files.zip'), compression='zip')

### ETL ### 
# # load geoview metadata and shape files
# metadata = pd.read_csv(os.path.join('data','geoview','capstone_metadata.zip'),
#     compression='zip', parse_dates=['report_year','date_from','date_to'],
#     usecols=['anumber','title','report_type','project','keywords','commodity','report_year','date_from','date_to'])

# geoview = gpd.read_file(os.path.join('zip://','data', 'geoview', 'capstone_shapefiles.shp.zip'))

# ### ETL ###
# map_geometry = geoview.loc[geoview.anumber.isin(events.anumber)]
# map_geometry = map_geometry.loc[map_geometry.geometry.notna()]
# map_data = metadata.loc[metadata.anumber.isin(map_geometry.anumber),:]
# map_data['anumber_str'] = map_data['anumber'].astype(str)
# map_data['epoch'] = map_data.report_year.astype(np.int64).divide(1e9).astype(np.int64)

# # save to file
# map_data.to_csv('data/geoview/map_data.zip', compression={'method':'zip','archive_name':'map_data.csv'})
# map_geometry.to_file("data/geoview/map_geometry.shp")

## load data
map_data = pd.read_csv(os.path.join('data','geoview','map_data.zip'), compression='zip', index_col=0, parse_dates=['report_year','date_from','date_to'])
map_data['report_year'] = map_data['report_year'].dt.strftime('%Y')
map_data = map_data.merge(group_event_score(events), on='anumber')
map_data.score = map_data.score.round(4).multiply(100)

map_geometry = gpd.read_file(os.path.join('zip://','data', 'geoview', 'map_geometry.zip'), index_col=0)