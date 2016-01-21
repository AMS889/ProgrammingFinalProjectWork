# -*- coding: utf-8 -*-
"""
Date: December 10, 2015
Author: Alex Simonoff

This module includes a visualization class containing two main functionalities:
One function generates a basemap depending on the input zip code by borough and plots the 
predicted number of bikes at all stations in that borough at the time 
corresponding borough. Additionally it established the longitude and latitude limits of each borough
"""
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from VisualizationFunctions import citiBikeDataLoad, fullStationDataLoad, boroughDataLoad

class visualization(object):
    
    def __init__(self, inputzip, month, day, hour):
        #Stores variables to be used by class functions
        self.inputzip = int(inputzip)
        self.month = int(month)
        self.day = str(day)
        self.hour = int(hour)
    
    def basemapPlot(self, saveVar):
        #Upper and lower bounds for borough's latitudes and longitudes
        latsAndLongs={}
        latsAndLongs["ManhattanLowerLat"]=40.698545
        latsAndLongs["ManhattanUpperLat"]=40.800038
        latsAndLongs["ManhattanLowerLong"]=-74.022824
        latsAndLongs["ManhattanUpperLong"]=-73.904194
        latsAndLongs["BrooklynLowerLat"]=40.677046
        latsAndLongs["BrooklynUpperLat"]=40.740347
        latsAndLongs["BrooklynLowerLong"]=-74.010918
        latsAndLongs["BrooklynUpperLong"]=-73.921764
        latsAndLongs["QueensLowerLat"]=40.737877
        latsAndLongs["QueensUpperLat"]=40.756525
        latsAndLongs["QueensLowerLong"]=-73.962982
        latsAndLongs["QueensUpperLong"]=-73.929904
        
        #Loading borough information to be used in generating correct basemap
        boroughdf=boroughDataLoad()
        boroughdf=boroughdf.set_index('ZipCode')['Borough'].to_dict()
        boro=boroughdf[self.inputzip]
        
        #Loading Station Data to be used in slicing the citibike availability data
        stationData=fullStationDataLoad()
        boroStations=stationData['id'][stationData["Borough"]==boro].tolist()
        boroLats=stationData[['id','latitude']][stationData["Borough"]==boro]
        boroLons=stationData[['id','longitude']][stationData["Borough"]==boro]
        
        #Loading the citibike availability data and storing the relevent information into lists
        citidf=citiBikeDataLoad()
        citiStations = citidf.columns.values
        citiStations = citiStations.astype(int)
        boroStations = list(set(boroStations).intersection(citiStations))
        if len(boroStations)==0:
            print "There are no bike stations in this area"
        else:
            #Plotting the basemap
            plt.figure(figsize=(14,14))
            m = Basemap(resolution='h',
                        projection='mill',
                        llcrnrlat = latsAndLongs[boro+"LowerLat"],
                        llcrnrlon = latsAndLongs[boro+"LowerLong"],
                        urcrnrlat = latsAndLongs[boro+"UpperLat"],
                        urcrnrlon = latsAndLongs[boro+"UpperLong"],
                        area_thresh = 0.1)
            m.drawcountries(linewidth=0.5)
            m.drawcoastlines(linewidth=0.5)
            m.drawstates(linewidth=0.5)
            m.fillcontinents(color = 'lightgray')
            
            #Storing data in lists to be plotted
            bikes=[]
            lats=[]
            lons=[]
            for stations in boroStations:
                bikes.append(int(citidf.loc[self.day, self.hour, self.month].ix[str(stations)]))
                lats.append(float(boroLats['latitude'][stationData["id"]==stations]))
                lons.append(float(boroLons['longitude'][stationData["id"]==stations]))
            
            #Plotting the stations on top of the basemap
            minMarkerSize = .4
            for bikes, lats, lons in zip(bikes, lats, lons):
                x,y = m(lons, lats)
                msize = bikes * minMarkerSize
                m.plot(x, y, 'bo', markersize=msize)
            plt.title('Predicted Number of Bikes In '+str(boro)+' on '+self.day+'s in Month '+str(self.month)+" at "+str(self.hour))

            if saveVar=="Y":
                #Saves plot depending on user input
                plt.savefig('MapOfCitiBikeAvailabilityFor'+self.day+'sInMonth'+str(self.month)+'atHour'+str(self.hour)+'.pdf')
            else:
                pass
            return m
    
    def barPlot(self, saveVar):
        bikesByStation={}
        bikesForDict=[]
        stationsForDict=[]
        
        #Loading Station Data to be used in slicing the citibike availability data
        stationData=fullStationDataLoad()
        zipStations=stationData['id'][stationData["postalCode"]==self.inputzip].tolist()
        #Loading citibike availability data
        citidf=citiBikeDataLoad()
        citiStations = citidf.columns.values
        citiStations = citiStations.astype(int)
        zipStations = list(set(zipStations).intersection(citiStations))
        if len(zipStations)==0:
            print "There are no bike stations in this zip code"
        else:
            #Storing plot values and labels
            for stations in zipStations:
                bikesForDict.append(int(citidf.loc[self.day, self.hour, self.month].ix[str(stations)]))
                stationsForDict.append(str(stationData.loc[str(stations)].ix['stationName']).strip())
            #Storing plot values and labels into dictionary for easy use
            bikesByStation=dict(zip(stationsForDict, bikesForDict))
            
            #Plotting bikes by station using a barchart
            plt.figure(figsize=(14,14))
            width = 1
            plt.bar(range(len(bikesByStation)), bikesByStation.values(), width, color='mediumpurple', align='center')
            plt.xticks(range(len(bikesByStation)), bikesByStation.keys(), rotation=70, fontsize=12, ha="right")
            plt.xlim([-1,len(bikesByStation)])
            plt.title('Predicted Number of Bikes For '+self.day+'s in Month '+str(self.month)+" at "+str(self.hour)+' In ZipCode '+str(self.inputzip), fontsize=12)
            plt.xlabel('Station', fontsize=12)
            plt.ylabel('Predicted Number of Bikes', fontsize=12)
            plt.show()    
            if saveVar == "Y":
                #Saves plot depending on user input
                plt.savefig('PlotOfCitiBikesAvailableOn'+self.day+'sMonth'+str(self.month)+'Hour'+str(self.hour)+'Zip'+str(self.inputzip)+'.pdf')
            else:
                pass

