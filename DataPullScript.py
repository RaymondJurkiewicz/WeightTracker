#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 02:27:39 2022

@author: rjurkiewicz

This script pulls the data from the API and saves it as a csv 

"""

import pandas as pd

import gspread
from oauth2client.service_account import ServiceAccountCredentials


#Set up and conenct to API

scope = ["https://spreadsheets.google.com/feeds",
         'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("autology_credentials.json", scope)

client = gspread.authorize(creds)

sheet = client.open("Weight Tracker").sheet1

data = sheet.get_all_records()

#save as csv

dataFrame = pd.DataFrame(data)
dataFrame.to_csv('Autology_Data.csv')


