import numpy as np
import pandas as pd
import geopandas as gpd
import os

def report_scores(events, by_anumber=True):
    '''Takes the events dataframe as input with filename and anumber in columns.
    Groups by filename or a_number to produce a report score given each identified event computed by
    product sum of (1 - P'(X)), a score analogous to the likelihood of at least one event assuming indepence
    '''
    # whether to group by filename or anumber    
    groupby_col = 'anumber' if by_anumber else ['anumber','filename']
    
    # grouped dataframe with report score
    df = events.groupby(groupby_col).prob.apply(
        lambda x : x.subtract(1).multiply(-1).prod()
    ).fillna(1).multiply(-1).add(1)
    
    # rename prob of each event to score for report
    df.name = 'score'  # report score between 0 and 1
    df = df.reset_index()
    
    # add num of near misses and total extracted text chunks
    df['count'] = events.groupby(groupby_col).label.sum().values  # number of near miss text chunks
    df['total'] = events.groupby(groupby_col).label.count().values  # number of text chunks
    df['prop'] = df['count']/df['total']  # proportion of near miss text chunks
    
    return df

# commodities = pd.read_csv(os.path.join('data','commodities_high-conf.csv'),index_col=0) # originally for commodities dropdown
# capstone_files = pd.read_csv(os.path.join('data','capstone_files.zip'), compression='zip')

### ETL ### 
# # load geoview metadata and shape files
# metadata = pd.read_csv(os.path.join('data','geoview','capstone_metadata.zip'),
#     compression='zip', parse_dates=['report_year','date_from','date_to'],
#     usecols=['anumber','title','report_type','project','keywords','commodity','report_year','date_from','date_to'])

# geoview = gpd.read_file(os.path.join('zip://','data', 'geoview', 'capstone_shapefiles.shp.zip'))

# map_geometry = geoview.loc[geoview.anumber.isin(events.anumber)]
# map_geometry = map_geometry.loc[map_geometry.geometry.notna()]
# map_data = metadata.loc[metadata.anumber.isin(map_geometry.anumber),:]
# map_data['anumber_str'] = map_data['anumber'].astype(str)
# map_data['epoch'] = map_data.report_year.astype(np.int64).divide(1e9).astype(np.int64)

#  save to file
# map_data.to_csv('data/geoview/map_data.zip', compression={'method':'zip','archive_name':'map_data.csv'})
# map_geometry.to_file("data/geoview/map_geometry.shp")
### ETL ###