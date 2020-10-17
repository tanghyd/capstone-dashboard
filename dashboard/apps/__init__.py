import pandas as pd
import geopandas as gpd

# load data
dataframe = pd.read_csv('data/events.csv')
dataframe['label'] = dataframe['label'].astype(int)
#dataframe = pd.read_csv('data/group_all_labelled.csv', nrows=500)
#dataframe['labels'] = dataframe['Near Miss Event'].astype(int)

capstone_files = pd.read_csv('data/capstone_files.zip', compression='zip')

# load geoview metadata and shape files
metadata = pd.read_csv('data/geoview/capstone_metadata.zip', compression='zip', parse_dates=['report_year'],
    usecols=['anumber','title','report_type','project','keywords','commodity','report_year'])
geoview = gpd.read_file('zip://data/geoview/capstone_shapefiles.shp.zip')

from pipeline.processing import load_spacy_model
nlp = load_spacy_model(output_type='doc', trigger_matcher=True, lemmatizer=False, geological_matcher=True,
                       stopword_removal=False, punctuation_removal=False, lemmatize_triggers=True)