#!/usr/bin/env python
# coding: utf-8

# In[38]:


##Problem Set 5


# In[141]:


## import the packages
import pandas as pd
import numpy as np
from scipy.optimize import minimize
from scipy.optimize import differential_evolution
from geopy.distance import geodesic


# In[142]:


# Read in the datafile
# 
df = pd.read_csv(r'C:\Users\PC\Desktop\radio_merger_data.csv')


# In[146]:


df.head(n = 10)


# In[147]:


#Create datasets for year 2007 and 2008
df2007=df[df['year'] == 2007 ]
df2008=df[df['year'] == 2008 ]


# In[150]:


# Calculate distances for years and the result in a matrix
def calc_distance(distance,buyer_lat, buyer_long, target_lat, target_long, start_index):
    for i in range(distance.shape[0]):
        for j in range(distance.shape[0]):
            distance[i,j] = geodesic((buyer_lat[i + start_index], buyer_long[i + start_index]),
                                    (target_lat[j + start_index],target_long[j + start_index])).miles
    return distance

# seperate buyers and targets into different groups by year and select their location
buyer_lat2007 = df2007.loc[:, 'buyer_lat']
buyer_long2007 = df2007.loc[:, 'buyer_long']
target_lat2007 = df2007.loc[:, 'target_lat']
target_long2007 = df2007.loc[:, 'target_long']

buyer_lat2008 = df2008.loc[:, 'buyer_lat']
buyer_long2008 = df2008.loc[:, 'buyer_long']
target_lat2008 = df2008.loc[:, 'target_lat']
target_long2008 = df2008.loc[:, 'target_long']

#calculate the distance
distance2007 = np.zeros((df2007.shape[0],df2007.shape[0]))
distance2007 = calc_distance(distance2007, buyer_lat2007,buyer_long2007, target_lat2007,target_long2007, 0)
distance2008 = np.zeros((df2008.shape[0],df2008.shape[0]))
distance2008 = calc_distance(distance2008, buyer_lat2008,buyer_long2008, target_lat2008,target_long2008, 45)


# In[163]:


# Define the MSE function
def mse(param, buyer_nsb, buyer_cob, population_per_mil, distance, start_index):
    '''
    param[0]:alpha, param[1]:beta
    '''
    result = 0
    estimate_fomula = np.zeros((distance.shape[0],distance.shape[0]))
    for i in range(distance.shape[0]):
        for j in range(distance.shape[0]):
            estimate_fomula[i,j] = buyer_nsb[i + start_index] * population_per_mil[j + start_index] + param[0] * buyer_cob[i + start_index] * population_per_mil[j + start_index] + param[1] * distance[i, j]
    
    for i in range(distance.shape[0] - 1):
        for j in range(i + 1, distance.shape[0]):
            if ((estimate_fomula[i,i] + estimate_fomula[j,j]) > (estimate_fomula[i,j] + estimate_fomula[j,i])):
                result = result + 1
    return -result

buyer_nsb_2007 = df2007.loc[:, 'num_stations_buyer']
buyer_cob_2007 = df2007.loc[:, 'corp_owner_buyer']
population_per_mil_2007 = df2007.loc[:,'population_target'] / 1000000

bounds = [(-1000,1000),(-1000,1000)]
arguments2007 = (buyer_nsb_2007, buyer_cob_2007, population_per_mil_2007, distance2007, 0)
max_result2007 = differential_evolution(mse, bounds, args = arguments2007, strategy = 'best1bin', maxiter = 10000)

buyer_nsb_2008 = df2008.loc[:, 'num_stations_buyer']
buyer_cob_2008 = df2008.loc[:, 'corp_owner_buyer']
population_per_mil_2008 = df2008.loc[:,'population_target'] / 1000000

bounds = [(-1000,1000),(-1000,1000)]
arguments2008 = (buyer_nsb_2008, buyer_cob_2008, population_per_mil_2008, distance2008, 45)
max_result2008 = differential_evolution(mse, bounds, args = arguments2008, strategy = 'best1bin', maxiter = 10000)

#print the result
print(max_result2007.x, max_result2008.x)


# In[185]:


#Define the second MSE function
def mse_2(param, buyer_nsb, buyer_cob, hhi_target ,population_per_mil, price_per_mil, distance, start_index):
    '''
    param[0]:delta, param[1]:alpha, param[2]:gamma, param[3]:beta
    '''
    result = 0
    estimate_fomula = np.zeros((distance.shape[0],distance.shape[0]))
    for i in range(distance.shape[0]):
        for j in range(distance.shape[0]):
            estimate_fomula[i,j] = param[0] * buyer_nsb[i + start_index] * population_per_mil[j + start_index] + param[1] * buyer_cob[i + start_index] * population_per_mil[j + start_index] + param[2] * hhi_target[j + start_index] + param[3] * distance[i, j]
    
    for i in range(distance.shape[0] - 1):
        for j in range(i + 1, distance.shape[0]):
            if ((estimate_fomula[i,i] - estimate_fomula[i,j]) > (price_per_mil[i + start_index] - price_per_mil[j + start_index]) and (estimate_fomula[j,j] - estimate_fomula[j,i]) > price_per_mil[j + start_index] - price_per_mil[i + start_index] ):
                result = result + 1
    return -result

## for the year 2007
price_per_mil_2007 = df2007.loc[:, 'price'] / 1000000
hhi_target2007 = df2007.loc[:, 'hhi_target']

bounds = [(-1000,1000),(-1000,1000),(-1000,1000),(-1000,1000)]
arguments2007 = (buyer_nsb_2007, buyer_cob_2007, hhi_target2007, population_per_mil_2007, price_per_mil_2007, distance2007, 0)
max_result2007 = differential_evolution(mse_2, bounds, args = arguments2007, strategy = 'best1bin', maxiter = 10000)

## for the year 2008
price_per_mil_2008 = df2008.loc[:,'price'] / 1000000
hhi_target2008 = df2008.loc[:, 'hhi_target']

bounds = [(-1000,1000),(-1000,1000),(-1000,1000),(-1000,1000)]
arguments2008 = (buyer_nsb_2008, buyer_cob_2008, hhi_target2008, population_per_mil_2008, price_per_mil_2008, distance2008, 45)
max_result2008 = differential_evolution(mse_2, bounds, args = arguments2008, strategy = 'best1bin', maxiter = 10000)

#print the result
print(max_result2007.x, max_result2008.x)


# In[ ]:




