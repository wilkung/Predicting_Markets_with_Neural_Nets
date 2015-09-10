from os import listdir
from os.path import isfile, join
import os
import glob
import datetime
import pandas as pd
from dateutil.parser import parse

SKIP=1

if SKIP!=1:
    #create list of all dates from 12/31/99 to 07/31/2015
    dt = datetime.datetime(1999, 12, 31)
    end = datetime.datetime(2015, 7, 31)
    step = datetime.timedelta(days=1)
    
    dates = []
    
    while dt < end:
    #    dates.append(dt.strftime('%Y-%m-%d %H:%M:%S'))
        dates.append(dt.strftime('%Y-%m-%d'))
        dt += step
        
    #write list of dates into master data file (data_file.txt)
    type( dates[0] )
    dates[0]
    
    data_file = open("data_file.txt", "w")
    
    data_file.write('Date' +"\n")
    for date in dates:
        data_file.write(date + ",\n")              
    
    data_file.close()
    
    # create 2 lists of daily filenames and weekly filenames in directory
    daily_directory = '/Users/wilsonkung/DataScience/metis/projects/project_kojak_wilsonkung/data/Daily'
    weekly_directory =  '/Users/wilsonkung/DataScience/metis/projects/project_kojak_wilsonkung/data/weekly'
    
    daily_files = [ f for f in listdir(daily_directory) if isfile(join(daily_directory, f)) and f[0] not in ['_', '.'] ]
    weekly_files = [ f for f in listdir(weekly_directory) if isfile(join(weekly_directory, f)) and f[0] not in ['_', '.'] ]
    
    data_df = pd.DataFrame.from_csv('data_file.txt',index_col=False)
    #data_df = pandas.read_csv('data_file.txt')
    
    
    #data_df = data_df.merge(temp_df[['Date','Values']], on='Date', how='left'
    
    x = 0
    
    for file in daily_files:
        print ( 'processing: '+ file + ' ' + str(x) )
        temp_df = pd.read_csv('./data/Daily/' + file)
        data_df = data_df.merge(temp_df[['Date','Values']], on='Date', how='left')
        data_df = data_df.rename(columns = { 'Values': 'D_' + file.split('.')[0] })
        x += 1
        
    #    data_df = data_df.merge(temp_df[list('Value')] , on='Date', how='left')
    #
    for file in weekly_files:
        print ( 'processing: '+ file + ' ' + str(x) )
        temp_df = pd.read_csv('./data/weekly/' + file)
        data_df = data_df.merge(temp_df[['Date','Values']], on='Date', how='left')
        data_df = data_df.rename(columns = { 'Values': 'W_' + file.split('.')[0] })
        x += 1

    data_df.to_csv('combined_data.csv')

FREQ =  5 #1
ASSUMED_WEEKLY_DATA_RELEASE = 'WEDNESDAY'
BEG_DATE = datetime.datetime(2002, 12, 31)


#datetime.datetime.today()
#datetime.datetime.today().weekday()

#################################################################################

PATH = '/Users/wilsonkung/DataScience/metis/projects/project_kojak_wilsonkung/'
data_df = pd.read_csv(PATH+'combined_data.csv')

cols = [c for c in data_df.columns if c[:2] == 'D_' or c == 'Date']
#
#
daily_data_df = data_df[cols]

daily_data_df_subset = daily_data_df[ pd.to_datetime( daily_data_df['Date']) >= BEG_DATE ]

feature_count = daily_data_df_subset.isnull().sum()