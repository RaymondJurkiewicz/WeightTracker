#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 28 17:57:00 2022
@author: rjurkiewicz
This code generates graphs of daily weight & calories
"""

# import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from datetime import date
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

##### Grab the Data

dataset = pd.read_csv('Autology_Data.csv')

##### Clean dataset

dataset = dataset[['Date', 
                   'Goal Weight', 
                   'Weight', 
                   'Goal Calories', 
                   'Calories']]

dataset.astype({'Goal Weight':'float',
           'Weight':'float',
           'Goal Calories':'float',
           'Calories':'float'
           })
dataset['Date'] = pd.to_datetime(dataset['Date'])


dataset.set_index('Date')
dataset = dataset.loc[(dataset['Date'] > '2022-05-01') & 
                      (dataset['Date'] <= date.today().strftime("%Y-%m-%d"))]

dataset['Weight'] = dataset['Weight'].interpolate(method = 'linear')

print(date.today().strftime("%Y-%m-%d"))

##### Add Weekly moving average

dataset['Weekly Avg Weight'] = dataset['Weight'].rolling(7).mean()
dataset['Weekly Avg Calories'] = dataset['Calories'].rolling(7).mean()
print(dataset)

####### Plot Weight

sns.set_style('dark')
sns.lineplot(x='Date', y='Weight', sort=False, data=dataset)
sns.lineplot(x='Date', y='Weekly Avg Weight', sort=False, data=dataset)

# Get the current Axes
plt.gcf().autofmt_xdate()

ax = plt.gca()
#edit x axies
#ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
ax.xaxis.set_major_locator(ticker.MultipleLocator(base=14))

plt.savefig('weight.png', dpi=300)

#show figure
plt.show()

####################################

sns.set_style('dark')
graph = sns.lineplot(x='Date', y='Calories', sort=False, data=dataset)
graph2 = sns.lineplot(x='Date', y='Weekly Avg Calories', sort=False, data=dataset)

graph.axhline(1800, c = 'black')

# Get the current Axes
plt.gcf().autofmt_xdate()

ax = plt.gca()
#edit x axies
#ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
ax.xaxis.set_major_locator(ticker.MultipleLocator(base=14))


plt.savefig('calories.png', dpi=300)

#show figure
plt.show()