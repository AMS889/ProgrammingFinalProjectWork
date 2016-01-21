# -*- coding: utf-8 -*-
"""
Date: December 1, 2015
Author: Alex Simonoff

This module generates and cleans the weather data for all days in our dataset
It then outputs the data to a csv to be used by our model
"""
import pandas as pd

def weatherDataLoad():
    dfNOAADaily = pd.DataFrame(pd.read_csv("DailyPrecipNOAA.csv"))
    return dfNOAADaily

def precipIndicator(weatherData):
    #Creating a precipitation indicator for any rainfall or snowfall on a given day
    weatherData['Precip'] = pd.Series((weatherData['PRCP'] + weatherData['SNOW']) > 0, dtype=int)
    return weatherData

def weatherDataDateColumn(weatherData):
    weatherData['dateCol']=0
    for i in range(len(weatherData)):
        weatherData['dateCol'][i] = '%s-%s-%s' % (str(weatherData['DATE'][i])[:4], str(weatherData['DATE'][i])[4:6],str(weatherData['DATE'][i])[6:8])
    return weatherData

def weatherWDateDataClean(weatherData):
    #Removing a row of unused/unnecessary data
    del weatherData['STATION']
    return weatherData

def storeWeatherData(weatherData):
    #Storing data for use by model
    weatherData.to_csv("WeatherDataCleaned.csv")