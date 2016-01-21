from DataClean import *

'''This module includes methods used to generate 'plus and minus' matrices for the Citibike Dataset. These matrices represent the change in number of bikes at each station during each hour over the three years of our Citibike data. Since we only have access to the start and end station IDs in the Citibike data, we thought that building these matrices was the best way to represent information about the number of bikes at each station given the time of day, or year.'''

path = "data/Citibike Data/"
df = pd.DataFrame(pd.read_csv("data/Citibike Data/2013-07 - Citi Bike trip data.csv"))
df = append_data(df, path)
df = add_columns(df)
datelist = pd.date_range('2013-07-01', periods=30000, freq='H').tolist()
station_id_list = list(df['end station id'].unique())

def generate_matrix(sign):
    '''This function generates the matrices described above, given the input 'plus' or 'minus' for postive change in bikes over each hour and negative change in bikes, respectively. First, we create an empty dataframe with the Citibike station IDs as columns, and an index of the hour by hour timestamp for 2013-2015'''
    df2 = pd.DataFrame(index=datelist, columns = station_id_list)
    df2 = df2.fillna(0)
    #insert values into plus matrix
    if sign == 'plus':
    #if we are generating the plus matrix, we consider all of the end station data, as in this case a bike is going to be returning to a station, hence +1.
        for ID, year, month, day, hour in zip(df['end station id'],df['stop_year'], df['stop_month'], df['stop_day'], df['stop_hour']):
            index = '{}-{}-{} {}:00:00'.format(year,month,day,hour)
            df2.ix[index, ID] += 1
    else:
    #in the other case, we only consider the start station data, as a bike will be leaving a station, hence -1.    
        for ID, year, month, day, hour in zip(df['start station id'],df['start_year'], df['start_month'], df['start_day'], df['start_hour']):
            index = '{}-{}-{} {}:00:00'.format(year,month,day,hour)
            df2.ix[index, ID] -= 1
    return df2[0:19008]  


def save_matrices():
    '''This function saves the plus and minus matrices so we can access them later on without generating them again. We also compute a net change matrix with is essentially the sum of the plus and minus matrices'''
    df_plus = generate_matrix('plus')
    df_minus = generate_matrix('minus')
    df_net = pd.DataFrame.add(df_plus, df_minus)
    df_plus.to_csv('PlusMatrix.csv')
    df_minus.to_csv('MinusMatrix.csv')
    df_net.to_csv('NetChangeMatrix.csv')
    
    
    