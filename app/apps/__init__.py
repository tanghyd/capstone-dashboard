import pandas as pd
dataframe = pd.read_csv('data/group_all_labelled.csv', nrows=50)
dataframe['labels'] = dataframe['Near Miss Event'].astype(int)

