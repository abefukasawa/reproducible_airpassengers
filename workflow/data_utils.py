from urllib.request import urlretrieve
import pandas as pd
import os
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima_model import ARIMA

def data_loading(url, filename, force_download=False):
    """
    Loads a dataset from some url and saves it in csv format to a filename
    
    Parameters
    -----------
    url [string]: 
        Contains our data in some web server.
    filaname [string]:
        Desired filename where the data will be downloaded.
    force_downloads [boolean]:
        User chooses wheter to forcefully download the data.
        
    
    Returns
    -----------
    df [pandas.DataFrame]
        Desired data in DataFrame
    """
    if not os.path.exists(filename):
        file_id = url.split('/')[-2]
        dwn_url='https://drive.google.com/uc?export=download&id=' + file_id
        urlretrieve(dwn_url, filename)
    else:
        pass
    df = pd.read_csv(filename)
    try:
        df['Month'] = pd.to_datetime(df.Month, format='%Y-%m')
    except TypeError:
        df['Month'] = pd.to_datetime(df.Month)
    #df = df.set_index('Month')
    df.rename(columns={'#Passengers':'Passengers'}, inplace=True)
    
    # Unit testing
    #assert all(df.columns == ['Passengers'])
    
    return df


def test_stationary(timeseries):
    """
    Applies the augmented Dickey-Fuller test to a given time series and prints
    its main statistics.
    
    Parameters
    ----------
    timeseries [pandas.DataFrame]:
        DataFrame with time index containing observations in sequence.
        
    Returns
    ---------
    [] only prints statistics
    """
    #Determining Rolling Statistics
    movingAverage = timeseries.rolling(window = 12).mean()
    movingStd = timeseries.rolling(window = 12).std()
    
    #Plotting Rolling Statistics
    plt.plot(timeseries, linewidth = 2, label = 'Original')
    plt.plot(movingAverage, linewidth = 2, label = 'Rolling Mean', color = 'r')
    plt.plot(movingStd, linewidth = 2, label = 'Rolling Std Dev', color = 'k')
    plt.legend(loc = 'best')
    plt.title('Rolling Mean and Standard Deviation')
    plt.show()
    
    #Performing Dickey Fuller Test
    #Performing Augumented Dickey Fuller Test
    print('Results of the Dickey Fuller Test')
    dftest = adfuller(x = timeseries['Passengers'], autolag= 'AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    print(dfoutput)
    for key,value in dftest[4].items():
        print('Critical Value ({}) = {}'.format(key,value))
        
