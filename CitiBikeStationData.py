# -*- coding: utf-8 -*-
"""
Date: December 3, 2015
Author: Alex Simonoff

This module builds out the data for all stations to link them to their zip codes for
the user input functionality/main program
"""
import pandas as pd
import urllib2

def stationDataLoad():
    #read json page into dataframe
    station_data = pd.read_json('http://www.citibikenyc.com/stations/json')
    return station_data

def stationDataClean(station_data):
    #need to separate column stationBeanList because it contains a dicitionary
    series_format = pd.Series(station_data['stationBeanList'])
    lst_format=list(series_format)
    station_data = pd.DataFrame(lst_format)
    station_data['city'] = 'New York'
    station_data = station_data.drop(station_data.columns[[0,5,8,12]], axis = 1)
    station_data = station_data[station_data["statusValue"]=="In Service"]
    station_data = station_data.reset_index(drop=True)
    return station_data

def postalCodeDataPull(station_data):
    station_data['postalCode']=0
    #Using an API to link the longitude and latitude data to the zip code associated with them
    for i in range(len(station_data[station_data['postalCode']==0])):
        link = ("https://api.factual.com/geotag?latitude=" + str(station_data["latitude"][i])+ "&longitude=" + str(station_data["longitude"][i])+"&KEY=Go6OJPfGhzlC6BcTGQBN8TXrlNQ90tkJTlk8sj8x")
        f = urllib2.urlopen(link).read()
        f2 = (f.split('"postcode":{"name":"')[1])[:5]
        station_data["postalCode"][i]=f2
    return station_data

def stationZipDataClean(station_data):
    #Selecting the relevant columns
    clean_station_data = station_data[['id','postalCode', 'latitude', 'longitude', 'stationName']]
    for i in range(len(clean_station_data)):
        clean_station_data['stationName'][i]=clean_station_data['stationName'][i].encode('utf-8')
    return clean_station_data

def boroughDataLoad():
    #importing csv which specifies borough by zip code and cleans the data
    boroughZips = pd.read_csv('boroughZips.csv')
    boroughZips = boroughZips[["ZipCode", "Borough"]]
    return boroughZips

def boroughDataMerge(clean_station_data, boroData):
    #importing csv which specifies borough by zip code and cleans the data
    stationWBoroData= clean_station_data.merge(boroData, left_on="postalCode", right_on="ZipCode", how="inner")
    stationWBoroData = stationWBoroData[['id','postalCode', 'latitude', 'longitude', 'stationName', "Borough"]]
    stationWBoroData = stationWBoroData.drop_duplicates()
    stationWBoroData = stationWBoroData.reset_index(drop=True)
    return stationWBoroData

def storeStationDataCSV(stationWBoroData):
    stationWBoroData.set_index("id")
    #Storing data for use by model
    stationWBoroData.to_csv("StationDataWZip.csv")