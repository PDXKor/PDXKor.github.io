# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 08:33:26 2020

@author: 15037
"""

#!/usr/bin/env python
import warnings
import pandas as pd

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

import json

class StockData():
    
    def __init__(self,ticker):
        self.ticker = ticker
        self.daily_close = self.get_historical_daily(self.ticker)
        self.balance_sheet = self.get_balancesheet_data(self.ticker)


    def get_jsonparsed_data(self,url):
        """
        Receive the content of ``url``, parse it as JSON and return the object.
    
        Parameters
        ----------
        url : str
    
        Returns
        -------
        dict
        """
        response = urlopen(url)
        data = response.read().decode("utf-8")
        return json.loads(data)
    
    def get_historical_daily(self,ticker):
        
        '''
        Gets daily stock data data via api call
        Parameters: ticker - string - the company stock ticker
        Returns: Dataframe, full or empty
        '''
        
        base_url = "https://financialmodelingprep.com/api/v3/historical-price-full/"
        request_url = base_url + ticker
        daily_data = self.get_jsonparsed_data(request_url)
        
        if not bool(daily_data):
            warnings.warn('Daily stock data could not be found. This could be due to an incorrect ticker value.')
            return pd.DataFrame()
            
        else:
            daily_df = pd.DataFrame(daily_data['historical'])  
            daily_df.index = daily_df['date']
            daily_df.index = pd.to_datetime(daily_df.index)
            return daily_df
        
    
    def get_balancesheet_data(self,ticker):
        
        '''
        Gets balance sheet data via api call
        Parameters: ticker - string - the company stock ticker
        Returns: Dataframe, full or empty
        '''
        
        base_url = "https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/"
        request_url = base_url + ticker + '?period=quarter'
        balance_sheet_data = self.get_jsonparsed_data(request_url)
                
        if not bool(balance_sheet_data):
            warnings.warn('Balance sheet data could not be found. This could be due to an incorrect ticker value.')
            return pd.DataFrame()
            
        else:
            balance_sheet_df = pd.DataFrame(balance_sheet_data['financials']) 
            balance_sheet_df.index = balance_sheet_df['date']
            balance_sheet_df.index = pd.to_datetime(balance_sheet_df.index)
            return balance_sheet_df




'''Testing'''

#APPL = StockData('AAPL')
#print(APPL.daily_close)
#print(APPL.balance_sheet.shape)

#appl_daily = get_historical_daily('AAPL')
#print(appl_daily)

#appl_balance_sheet = get_balancesheet_data('AAPL')
#print(appl_balance_sheet)

#appl_balance_sheet = get_balancesheet_data('APPL')
#print(appl_balance_sheet)

#url = ("https://financialmodelingprep.com/api/v3/company/profile/AAPL")
#print(get_jsonparsed_data(url))

#url = ("https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/AAPL")
#print(get_jsonparsed_data(url))

'''Analysis'''
# lets run principle component analysis to see which features from the balance sheet are most likely to influence the month long max of the balance sheet reporting date