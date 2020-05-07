# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 12:15:00 2020

@author: 15037
"""
import pyodbc
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, event

#conn = pyodbc.connect('DSN=reig-db-01;UID=reig-kmstaffo;PWD=T2exfrou')    
#cursor = conn.cursor()

engine=sqlalchemy.create_engine('mssql+pyodbc://reig-kmstaffo:T2exfrou@reig-db-01')
conn = engine.connect()   
@event.listens_for(engine, 'before_cursor_execute')
def receive_before_cursor_execute(conn, cursor, statement, params, context, executemany):
    print("FUNC call")
    if executemany:
        cursor.fast_executemany = True

def create_load_table_MedianAgeOfInventory_NSA_AllHomes_Metro(insert_base=True):   
         
    ''' Drops, creates and loads table for median inventory data'''    
    
    # read the csv into the dataframe
    df = pd.read_csv('MedianAgeOfInventory_NSA_AllHomes_Metro.csv')
    df = df.drop(columns=['RegionID','SizeRank'])
    df = df.melt(['RegionName','RegionType','StateName'], var_name='YearMonth', value_name='MedianAgeOfInventory')
    df['YearMonth'] = pd.to_datetime(df['YearMonth'])
    
    df.to_sql('median_inventory',engine,if_exists = 'replace',index=False,schema='dbo')
    print('done uploading zillow median inventory data')
    


def create_load_table_Stats_MedianAgeOfInventory_NSA_AllHomes_Metro(insert_base=True):   
         
    ''' Drops, creates and loads table for zillow rental table for all homes plus multifamily data'''    
    
    # read the csv into the dataframe
    df = pd.read_csv('MedianAgeOfInventory_NSA_AllHomes_Metro.csv')
    df = df.drop(columns=['RegionID','SizeRank'])
    df = df.melt(['RegionName','RegionType','StateName'], var_name='YearMonth', value_name='MedianAgeOfInventory')
    df['YearMonth'] = pd.to_datetime(df['YearMonth'])
    
    df = df.set_index("YearMonth")
    
    # get current year month
    df_stats = df[df['RegionName']=='Portland, OR']
    
    latst_inv =  df_stats.loc[df_stats.index.max()]['MedianAgeOfInventory']
    lst_yrs_inv = df_stats.loc[df_stats.index.max()- pd.DateOffset(years=1)]['MedianAgeOfInventory']
    lst_two_yrs_inv = df_stats.loc[df_stats.index.max()- pd.DateOffset(years=2)]['MedianAgeOfInventory']       
    print(latst_inv, lst_yrs_inv, lst_two_yrs_inv)
    
    
    #df.to_sql('median_inventory',engine,if_exists = 'replace',index=False,schema='dbo')
    #print('done uploading zillow median inventory data')
    
    
create_load_table_Stats_MedianAgeOfInventory_NSA_AllHomes_Metro()    




def create_load_table_Neighborhood_Zri_AllHomesPlusMultifamily(insert_base=True):
        
    ''' Drops, creates and loads table for zillow rental table for all homes plus multifamily data'''    
    
    # read the csv into the dataframe
    df = pd.read_csv('Zip_Zri_MultiFamilyResidenceRental.csv')
    df = df[(df['State']=='OR')&(df['Metro']=='Portland-Vancouver-Hillsboro')]
    df = df.drop(columns=['RegionID','State','SizeRank','Metro'])
    df = df.melt(['City', 'CountyName','RegionName'], var_name='YearMonth', value_name='AverageRent')
    df['YearMonth'] = pd.to_datetime(df['YearMonth'])
    df=df.rename(columns={'RegionName':'Zip'})
   
    df_stats = df
    df_stats = df_stats.set_index("YearMonth").last("18M")
    df_stats.sort_index()
    
    zips = df['Zip'].unique()
    
    for z in zips:
        plt.plot('YearMonth','AverageRent',data=df[df['Zip']==z])
        
    plt.show()
    
    if insert_base == True:
    
        # upload the relatively raw data
        df.to_sql('zillow_multifamily_rent',engine,if_exists = 'replace',index=False,schema='dbo')
         
        
    # TODO fix the code commented below to add summmary data to the db
    '''
     # create a df where the zip is the index
    zip_df = df[['Zip','CountyName','City']]#.unique()
    print(zip_df) 
    
    # create a df of the last 18 months to compute stats 
    df_stats = df
    df_stats = df_stats.set_index("YearMonth").last("18M")
    df_stats.sort_index()
    
    # let's determine the amount of increase from the first 6 months of the last 18 to the last 6 of the 18
    unique_dates = df_stats.index.unique().values
    first_three = unique_dates[0:3]
    last_three = unique_dates[-3:]
      
    df_stats.loc[first_three]
    '''
    
    print('done uploading zillow multi family rent data')
    

def create_load_table_MonthlyListings_NSA_AllHomes_Zip(insert_base=True):
    
    # Monthly For-Sale Inventory (Raw)
    df = pd.read_csv('MonthlyListings_NSA_AllHomes_Zip.csv')
    df = df.drop(columns=['RegionID','SizeRank'])
    df = df.melt(['RegionName','RegionType','StateName'], var_name='YearMonth', value_name='MonthlyListings')
    df['YearMonth'] = pd.to_datetime(df['YearMonth'])
    df = df.set_index("YearMonth")
    df= df[df['StateName']=='OR']
    # TODO fix automatically setting date range
    df = df.loc['2015-01-01':'2020-04-01']
    print(df)
    
    df.to_sql('monthly_listings',engine,if_exists = 'replace',index=True,schema='dbo')
    print('done uploading zillow median inventory data')
    
    
create_load_table_MonthlyListings_NSA_AllHomes_Zip()
#create_load_table_Neighborhood_Zri_AllHomesPlusMultifamily()
#create_load_table_MedianAgeOfInventory_NSA_AllHomes_Metro()
