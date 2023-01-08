#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 28 17:57:00 2022
@author: rjurkiewicz
This code generates graphs of daily weight & calories
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import date
import gspread
from oauth2client.service_account import ServiceAccountCredentials

#Set up and conenct to API

scope = ["https://spreadsheets.google.com/feeds",
         'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("/Users/rjurkiewicz/Desktop/Code/Autology/autology_credentials.json", scope)

client = gspread.authorize(creds)

sheet = client.open("Weight Tracker").sheet1

data = sheet.get_all_records()

# save as csv

dataset = pd.DataFrame(data)
dataset.to_csv('Autology_Data.csv')

##### Clean dataset

dataset = dataset.replace(r'^\s*$', np.nan, regex=True)

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
dataset = dataset.loc[(dataset['Date'] > '2022-03-01') & 
                      (dataset['Date'] <= date.today().strftime("%Y-%m-%d"))]

dataset['Weight'] = dataset['Weight'].interpolate(method = 'linear')


##### Add Weekly moving average

dataset['Weekly Avg Weight'] = dataset['Weight'].rolling(7).mean()
dataset['Weekly Avg Calories'] = dataset['Calories'].rolling(7).mean()



#################
## Plot Weight ##
#################

sns.set_style('dark')

weight = sns.lineplot(x='Date', y='Weight', sort=False, data=dataset, legend='full', label='weight')
weekly_avg_weight = sns.lineplot(x='Date', y='Weekly Avg Weight', sort=False, data=dataset, legend='full', label='weekly avg weight')
goal_weight = sns.lineplot(x='Date', y='Goal Weight', sort=False, data=dataset, legend='full', label='goal weight')

# Get the current Axes
plt.gcf().autofmt_xdate()

ax = plt.gca()

# Set the locator
locator = mdates.MonthLocator()  # every month
# Specify the format - %b gives us Jan, Feb...
fmt = mdates.DateFormatter('%b %Y')

ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(fmt)

plt.title('Weight Over Time')
plt.legend()
plt.grid()

plt.savefig('weight.png', dpi=300)

#show figure
plt.show()


###################
## Plot Calories ##
###################

sns.set_style('dark')
calories = sns.lineplot(x='Date', y='Calories', sort=False, data=dataset, legend='full', label='calories')
weekly_avg_calories = sns.lineplot(x='Date', y='Weekly Avg Calories', sort=False, data=dataset, legend='full', label='weekly avg calories')

calories.axhline(1800, c = 'black')

# Get the current Axes
plt.gcf().autofmt_xdate()

ax = plt.gca()

# Set the locator
locator = mdates.MonthLocator()  # every month
# Specify the format - %b gives us Jan, Feb...
fmt = mdates.DateFormatter('%b %Y')

ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(fmt)

plt.title('Calories Over Time')
plt.legend()
plt.grid()
plt.savefig('calories.png', dpi=300)

#show figure
plt.show()