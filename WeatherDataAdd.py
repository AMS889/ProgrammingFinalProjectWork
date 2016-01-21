from NetMatrixBuild import *
from DataClean import *


def weatherDataLoad():
    dfNOAADaily = pd.DataFrame(pd.read_csv("data/WeatherDataCleaned.csv"))
    return dfNOAADaily

def mergeWeatherData(weatherData, citiBikeData):
    weatherData2=weatherData[["dateCol", "Precip"]]
    mergedData=citiBikeData.merge(weatherData2, how = 'left', left_on="date", right_on="dateCol").set_index(citiBikeData.index)
    del mergedData["dateCol"]
    return mergedData

def generateNetWeatherNatrix():
    df_net = net_matrix_build()
    data = weatherDataLoad()
    df_weather = mergeWeatherData(data, df_net)
    df_weather['day of week'] = df_weather.index.map(lambda t: days[t.weekday()])
    df_weather['hour'] = df_weather.index.map(lambda t: t.hour)
    df_weather['month'] = df_weather.index.map(lambda t: t.month)
    testaggregation=df_weather[df_weather["Precip"] != 1].groupby(["day of week", "hour", "month"]).mean()
    testaggregation=np.round(testaggregation, 0)
    del testaggregation["Precip"]
    return testaggregation