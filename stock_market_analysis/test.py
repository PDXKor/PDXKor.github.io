# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 13:36:18 2020

@author: 15037
"""

import yfinance as yf



msft = yf.Ticker("MSFT")
print(msft)
print(msft.info)
print(msft.history(period="max"))


msft = yf.Ticker("DDM")
print(msft)
print(msft.info)
print(msft.history(period="max"))