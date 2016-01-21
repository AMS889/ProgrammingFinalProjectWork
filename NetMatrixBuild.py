from DataClean import *
from GenerateMatrices import *
import pandas as pd

'''This module includes a function to load a new dataset from Citibike that includes the total number of bikes at each station, so we can more accurately predict the expected number of bikes at a given time. Once we have that dataframe, we add that information to our net change dataframe, which has been loaded and saved as a csv in GenerateMatrices.'''

#read in our net change dataframe and our station dataframe with the total docks information
df_net = pd.DataFrame.from_csv('NetChangeMatrix.csv', index_col=0)
station_data = pd.read_json('http://www.citibikenyc.com/stations/json')

def clean_station_data(data):
    '''This function takes in the station data and cleans it, as we are mainly only interested in the total number of bikes ie. totalDocks at each station'''
    
    data = data.drop('executionTime',axis=1)
    data.columns = ['Total Docks']
    rows, columns = data.shape
    data['Station ID'] = 0
    station_id = []
    for r in range(rows):
        tot_docks = data['Total Docks'][r]['totalDocks']
        station_id.append(data['Total Docks'][r]['id'])
        data['Total Docks'][r] = tot_docks
    #here we create a guess column, where we make an assumption that when our Citibike data begins (July 1, 2013) there are approximately 1/2 of the total available bikes at each station, since it is unreasonale to assume that each station is full of bikes.    
    data['Available Docks Guess'] = data['Total Docks']//(2)
    data['Station ID'] = station_id
    data = data.set_index('Station ID')
    return data

station_data = clean_station_data(station_data)

def net_matrix_build(data, station_data):
    '''This function adds the information about the total bikes at station to our net matrix, which currently only contains small integers that represent the net change in bikes over each hour.'''
    for column in data.columns:
        try:
            #we add the values from the Available Docks Guess to the first row of our net change matrix (which represents the first hour of July 1, 2013)
            for i in range(793):
                data.ix[24*i, column] += station_data.ix[int(column), 'Available Docks Guess']
        except:
            continue
    #finally, we compute a rolling sum over the columns of the net change matrix        
    data = pd.rolling_sum(data.fillna(False), window = 24, min_periods = 1) 
    return data

df_net = net_matrix_build(df_net, station_data)