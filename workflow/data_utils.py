from urllib.request import urlretrieve
import pandas as pd
import os

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
    
    file_id = url.split('/')[-2]
    dwn_url='https://drive.google.com/uc?export=download&id=' + file_id
    urlretrieve(dwn_url, filename)
    df = pd.read_csv(filename)
    df['Month'] = pd.to_datetime(df.Month)
    return df