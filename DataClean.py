import pandas as pd
import numpy as np
import re
import os
import datetime

'''This module contains methods used to load and clean the Citibike dataset.'''

def append_data(data_frame, path):
    #append more csv files to dataframe, to create complete dataset        
    for f in os.listdir(path):
        if f.endswith(".csv") and not f.startswith("2013-07"): 
            newdf=pd.DataFrame(pd.read_csv(path + f))
            data_frame=data_frame.append(newdf, ignore_index=True)
    return data_frame  


def date_split(col_name, data_frame):
    '''This function takes in a time column of a dataframe, and that dataframe, and splits the time column into the month, year, hour, day, and day of the week. It appends all of these values to different lists, and returns the lists.'''
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    month = []
    day = []
    year = []
    hour = []
    day_of_week = []
    
    for ln in data_frame[col_name]:
        lst = ln.split(' ')
        #some of the values in the time column have different formats, so we need to try them all
        try:
            date = datetime.datetime.strptime(str(lst[0]), '%Y-%m-%d')
        except:
            date = datetime.datetime.strptime(str(lst[0]), '%m/%d/%Y')
        try:
            time = datetime.datetime.strptime(str(lst[1]), '%H:%M:%S')
        except:
            time = datetime.datetime.strptime(str(lst[1]), '%H:%M') 

        month.append(date.month)
        year.append(date.year)
        hour.append(time.hour)
        day.append(date.day)
        day_of_week.append(days[date.weekday()]) 
    return month, year, hour, day, day_of_week

def add_columns(data_frame):
    '''This function adds the month, year, hour, day, and day of the week lists that are returned by date_split to the dataframe that is input.'''
    
    month, year, hour, day, day_of_week = date_split('starttime', data_frame)
   
    data_frame['start_month'] = month
    data_frame['start_year'] = year
    data_frame['start_hour'] = hour
    data_frame['start_day'] = day
    data_frame['start_day_of_week'] = day_of_week
    
    month, year, hour, day, day_of_week = date_split('stoptime', data_frame)
    
    data_frame['stop_month'] = month
    data_frame['stop_year'] = year
    data_frame['stop_hour'] = hour
    data_frame['stop_day'] = day
    data_frame['stop_day_of_week'] = day_of_week
    
    return data_frame

