# -*- coding: utf-8 -*-
"""
Date: December 10, 2015
Author: Alex Simonoff

This module includes the dataload functions that are to be used by the visualization class
"""
import pandas as pd

def fullStationDataLoad():
    #loads the station dataframe
    station_data = pd.read_csv('StationDataWZip.csv', index_col=0)
    station_data["stringID"] = station_data["id"].astype(str)
    station_data = station_data.set_index('stringID')
    return station_data

def citiBikeDataLoad():
    #loads the number of expected bikes dataframe
    citiBikeData = pd.DataFrame(pd.read_csv("AggregatedDF.csv"))
    citiBikeData = citiBikeData.set_index(['day of week', 'hour', 'month'])
    citiBikeData[citiBikeData < 0] = 0
    return citiBikeData

def boroughDataLoad():
    #importing csv which specifies borough by zip code and cleans the data
    boroughZips = pd.read_csv('boroughZips.csv')
    boroughZips = boroughZips[["ZipCode", "Borough"]]
    return boroughZips
