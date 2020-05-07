# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pyodbc
import time

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# read the index google sheet
INDEX_SHEET_ID = '1kG2twLLJqEi3C9iB1xn-7twL4WhfffJyc-TM_kL1gUU'
INDEX_RANGE_NAME = 'index!A2:C100'

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # read the index sheet, to get the unique IDs for which sheets to read
    index_sheet = service.spreadsheets()
    index_result = index_sheet.values().get(spreadsheetId=INDEX_SHEET_ID,
                                range=INDEX_RANGE_NAME).execute()
    index_values = index_result.get('values', [])
    print(index_values)    
    
    if not index_values:
        # todo add logging
        print('no index data found')

    else:
        for row in index_values:
            
            # get the project spreadsheet
            project_spreadsheet_id = row[1]
            print(project_spreadsheet_id)
            project_range_name = 'project summary!A1:C50'
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=project_spreadsheet_id,
                                range=project_range_name).execute()
            values = result.get('values', [])
            #print(values) 
            
            project_dict = {}            
            if not values:
                # setup logging 
                print('No data found.')
        
            else:    
                for row in values:    
                    # if row len is two it has values we want to save
                    if len(row) == 3:
                        #print(row[1],row[2])
                        project_dict[row[1]]=row[2]

            conn = pyodbc.connect('DSN=reig-db-01;UID=reig-kmstaffo;PWD=T2exfrou')    
            cursor = conn.cursor()

            # check if the project name already exists
            # if so - run an update, if not run an insert
            name_check_sql = "select * from project_overview where name = '"+str(project_dict['name'])+"'"
            
            cursor.execute(name_check_sql)
            row = cursor.fetchone()
            print(row)
            # if a row exists then do an update
            # to make this quick we're doing a delete and insert
            # TODO make this an update
            if row:
                
                sql_stmt = "delete from project_overview where name = '"+str(project_dict['name'])+"'"
                del_cursor = conn.cursor()
                del_cursor.execute(sql_stmt)
                del_cursor.commit()
                
                insrt_cursor = conn.cursor()
                
                
                placeholder = ", ".join(["?"] * len(project_dict))
                sql_stmt = "insert project_overview ({columns}) values ({values});".format(columns=",".join(project_dict.keys()), values=placeholder)
                
                insrt_cursor.execute(sql_stmt,list(project_dict.values()))
                insrt_cursor.commit()
                
            else:
                placeholder = ", ".join(["?"] * len(project_dict))
                sql_stmt = "insert into project_overview ({columns}) values ({values});".format(columns=",".join(project_dict.keys()), values=placeholder)
            
                cursor.execute(sql_stmt,list(project_dict.values()))
                cursor.commit()
    
   


if __name__ == '__main__':
    main()