import bs4 as bs
from collections import Counter
import datetime as dt
from datetime import datetime,date
import calendar
import csv

import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np

import os
import pandas as pd
import pandas_datareader.data as web
import pickle
import requests
import sys




#Poloniex API#
import urllib
import urllib.request
import json
import time
import hmac,hashlib


style.use('ggplot')

## Pulls coin names from a space seperated text file
def read_crypto_file():
    file = open('coins.txt','r')
    coins = file.read().splitlines()
    return coins
    




## Pulls data from Poloniex API between the start and end dates.
## "Start" and "end" are given in UNIX timestamp format and used 
## to specify the date range for the data returned.
## Candlestick period in seconds; valid values are 
## 300 (5 minutes), 900 (15 minutes), 1800 (30 minutes), 
## 7200 (2 hours), 14400 (4 hours), and 86400 (1 day)

def get_data_from_polo():
    

    tickers = read_crypto_file()
 

    start_date = date(2017,1,1)
    timestamp1 = calendar.timegm(start_date.timetuple())
    start = timestamp1

    end_date = date(2017,3,27)
    timestamp2 = calendar.timegm(end_date.timetuple())
    end = timestamp2
    
    if not os.path.exists('coin_dfs'):
        os.makedirs('coin_dfs')
 
## Candlestick period valid values are 300, 900, 1800, 7200, 14400, and 86400
    period = 86400
        

    for ticker in tickers:
 
## Creates a seperate CSV file for each coin.
        if not os.path.exists('coin_dfs/{}.csv'.format(ticker)):
            print(ticker)
            df = urllib.request.urlopen('https://poloniex.com/public?command=' + "returnChartData" + '&currencyPair=' + 'BTC_'+ str(ticker) + '&start=' + str(start) + '&end=' + str(end) +'&period=' + str(period)) 
            str_info = df.read().decode('utf-8')
            info = json.loads(str_info)
            with open('coin_dfs/{}.csv'.format(ticker),'w',encoding='utf8') as f:
                writer = csv.DictWriter(f, fieldnames=['date','high','low','open','close','quoteVolume', 'weightedAverage','volume'])
                print(info)
                writer.writeheader()
                writer.writerows(info)

## Wait after every API call, as a precaution
            time.sleep(5)

        else:
            print('Already have{}'.format(ticker))
   
def compile_data():
    
    get_data_from_polo()

    tickers = read_crypto_file()
    
    main_df = pd.DataFrame()

    for count,ticker in enumerate(tickers):
        df = pd.read_csv('coin_dfs/{}.csv'.format(ticker))
        df.set_index('date', inplace=True)

        df.rename(columns = {'close':ticker}, inplace=True)
        df.drop(['high','low','open','quoteVolume','weightedAverage','volume'], 1, inplace=True)
        
        if main_df.empty:
            main_df = df    
        else:
            main_df = main_df.join(df,how='outer')

## Show Progress
        if count % 10 == 0:
            print(count)

    print(main_df.head())
    main_df.to_csv('coin_joined_closes.csv')

def visualize_data():
    compile_data()
    df = pd.read_csv('coin_joined_closes.csv')
    df.drop(['date'], 1, inplace=True)
    
    df_corr = df.corr()
    
    print(df_corr.head())
    
    data = df_corr.values
    fig = plt.figure()

## Chart layout options
    ax = fig.add_subplot(1,1,1)
    
    heatmap = ax.pcolor(data, cmap=plt.cm.RdYlGn)
    fig.colorbar(heatmap)
    ax.set_xticks(np.arange(data.shape[0]) +0.5, minor=False)
    ax.set_yticks(np.arange(data.shape[1]) +0.5, minor=False)
    ax.invert_yaxis()
    ax.xaxis.tick_top()
    
    column_labels = df_corr.columns
    row_labels = df_corr.index

    ax.set_xticklabels(column_labels)
    ax.set_yticklabels(row_labels)
    plt.xticks(rotation=90)
    heatmap.set_clim(-1,1)
    plt.tight_layout()
    plt.show()

visualize_data()