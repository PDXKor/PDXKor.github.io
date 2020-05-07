# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 20:57:53 2020
@author: 15037
"""

import yfinance as yf
import pandas as pd
import os

# set pandas options to show all columns
pd.set_option('display.max_columns',None)

# remove max column legth
pd.set_option('max_colwidth',None)

# make the table width longer
pd.set_option('display.width',1000)

files = os.listdir()
df = pd.read_csv('sp500_tickers.csv')

stock_hist_df = pd.DataFrame()

# build one large dataframe for each ticker in the sp500
for ticker in df['Symbol'].values[0:10]: 
    ticker_obj = yf.Ticker(ticker)
    ticker_history = ticker_obj.history(period='90d')
    ticker_history['Symbol'] = ticker
    stock_hist_df = stock_hist_df.append(ticker_history)
    if ticker_obj._institutional_holders is not None:
        print(ticker_obj.recommendations)
        
        
print(stock_hist_df)
    
# find stocks with the biggest change over the last 90 days
print(stock_hist_df.groupby(['Symbol'])['Close'].max().min())

summary_df = stock_hist_df.groupby(['Symbol']).agg(
    max_price=('Close',max),
    min_price=('Close',min),
    avg_price=('Close','mean'),
    last_price=('Close','last')
    )

summary_df['max_to_min_change'] = summary_df['max_price'] - summary_df['min_price']
summary_df['max_to_min_change_percent'] = (summary_df['max_price'] - summary_df['min_price'])/summary_df['max_price']
summary_df['rebound_potential_percent'] = (summary_df['max_price'] - summary_df['min_price'])/summary_df['last_price']

summary_df = summary_df.sort_values(['rebound_potential_percent'],ascending=False)

print(summary_df)

#summary_df.to_csv('rebound_potential_list.csv')