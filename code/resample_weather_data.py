
import pandas as pd
from datetime import datetime
import numpy as np
import datamanager as dm


#w_data = dm.get_weather_data()
#e_data = dm.get_industrial_electricity_data()
#print(w_data)
#print(e_data)

def print_head_and_tail(data_frame, note_str=None):
    if note_str:
        print('\n')
        print(note_str)
        #print('\n')
    print('\nHEAD -------------------------------------------------------------')
    print(data_frame.head())
    print('\nTAIL -------------------------------------------------------------')
    print(data_frame.tail())
    print('\n')


file_h = pd.ExcelFile('../weather_rome.xls')

# read data from excel, don't specify index (will be created)
df = pd.read_excel(file_h, sheet_name='rome', header=6) #, parse_dates=True) # ,index_col=0)

# drop extra columns/data
weather_data = df.drop(columns=['P0', 'WW', 'DD', 'ff10', "W'W'", 'c', 'VV'])

# rename date column "Local time in Ciampino (airport)" -> Datetime
weather_data = weather_data.rename(columns={"Local time in Ciampino (airport)": "DateTime"})

# helper column containing the original order (index) 
# (from the most resent date to the oldest)
weather_data['orig_order'] = range(0, len(weather_data))

#print_head_and_tail(weather_data)

# shape of the data
print('\nShape of the weather data:', weather_data.shape)

# missing values, empty cells
missing_values_list = weather_data.isnull().sum()
print('\nMissing values per column ----------------------------------------')
print(missing_values_list) # only two values missing, from Tf column, this is insync with the parse script

total_cells = np.product(weather_data.shape)
total_missing = missing_values_list.sum()

# Explicit datatime conversion
# 18.05.2018 23:50  
# https://medium.com/jbennetcodes/dealing-with-datetimes-like-a-pro-in-pandas-b80d3d808a7f
weather_data['DateTime'] = pd.to_datetime(weather_data['DateTime'], format='%d.%m.%Y %H:%M', utc=True)

# store the DateTime column value to new column
weather_data['orig_datetime'] = weather_data['DateTime']

# set the DateTime column as the new index for the weather_data
weather_data = weather_data.set_index('DateTime')

print_head_and_tail(weather_data)

# merge (resample) data by hour
# https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.resample.html
# http://benalexkeen.com/resampling-time-series-data-with-pandas/
# https://stackoverflow.com/questions/30857680/pandas-resampling-error-only-valid-with-datetimeindex-or-periodindex
#weather_data.index = pd.to_datetime(weather_data.index)
#print_head_and_tail(weather_data, 'after index to_datetime conversion')

# this messes up the date index
weather_resampled = weather_data.resample('H').mean()

print_head_and_tail(weather_resampled, 'after resampling by HOUR')

# check the shape 
print('\nShape of the weather_resampled data:', weather_resampled.shape)

# drop the extra orig_order column
weather_resampled = weather_resampled.drop(columns=['orig_order'])

# Any missing values?
missing_values_list = weather_resampled.isnull().sum()
print('\nMissing values per column ----------------------------------------')
print(missing_values_list)

# save to csv
weather_resampled.to_csv('../hourly_resampled_weather_data.csv')


