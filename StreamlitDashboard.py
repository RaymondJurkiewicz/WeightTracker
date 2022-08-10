#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 28 17:57:00 2022

@author: rjurkiewicz

This code generates a streamlit dashboard

"""

# import numpy as np
import pandas as pd
# import plotly as py

import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


##### Grab the Data

dataset = pd.read_csv('Autology_Data.csv')

##### Clean dataset


dataset = dataset[['Date', 
                        'Goal Weight', 
                        'Weight', 
                        'Goal Calories', 
                        'Calories']]


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
ax.xaxis.set_major_locator(ticker.MultipleLocator(base=21))

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
ax.xaxis.set_major_locator(ticker.MultipleLocator(base=21))


plt.savefig('calories.png', dpi=300)

#show figure
plt.show()




