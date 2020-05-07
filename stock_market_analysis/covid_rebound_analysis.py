# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 14:14:29 2020
@author: 15037
"""

from datetime import datetime
from datetime import timedelta
import numpy as np
from acies import StockData as sd
import pandas as pd

# set pandas options to show all columns
pd.set_option('display.max_columns',None)

# remove max column legth
pd.set_option('max_colwidth',None)

# make the table width longer
pd.set_option('display.width',1000)

# get the current list of sp500 tickers
df = pd.read_csv('sp500_tickers.csv')

# create a dictionary of stock objects for sp500
sp500_stock_objs = {}

# create a df to capture sp500 close data
sp500_close_data = pd.DataFrame()

# loop through the csv file and create a stock object for each
for ticker in df['Symbol'].values[0:2]: 
    stock_obj = sd(ticker)
    sp500_stock_objs[ticker]=stock_obj
    print(stock_obj.daily_close)
    
    # create a new column that is the ticker
    stock_obj.daily_close['Symbol'] = ticker
    
    # limit the range to the last one hundred days
    end_date = pd.Timestamp.today()
    begin_date = end_date - np.timedelta64(100,'D')    
    stock_obj.daily_close = stock_obj.daily_close.iloc[stock_obj.daily_close.index.get_loc(begin_date,method='nearest'):stock_obj.daily_close.index.get_loc(end_date,method='nearest')]
    
    print(stock_obj.balance_sheet.columns)    
    #print(stock_obj.daily_close)
    
print(sp500_stock_objs)



'''
# create a feature set that is the balance sheet data and the average stock price a month after reporting
aapl = sd('AAPL')
print(aapl.balance_sheet.columns)
print(aapl.balance_sheet.index)
print(aapl.daily_close)

aapl.balance_sheet['ten_day_avg_close'] = None 

for date in aapl.balance_sheet.index.values[0:10]:
    
    # get the average close price of the next 10 days after the balance sheet
    end_date = date + np.timedelta64(10,'D')
    close_values = aapl.daily_close.iloc[aapl.daily_close.index.get_loc(date,method='nearest'):aapl.daily_close.index.get_loc(end_date,method='nearest')]['close'].values
    avg_close = np.mean(close_values)
    aapl.balance_sheet.loc[date]['ten_day_avg_close'] = avg_close
    
aapl.balance_sheet = aapl.balance_sheet.dropna()   
print(aapl.balance_sheet)
'''
