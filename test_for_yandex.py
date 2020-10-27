#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import pandas as pd 
import numpy as np 

user_coord = pd.DataFrame()
user_coord = pd.read_csv('user_coordinates.csv')
user_coord


# In[82]:


place_coord = pd.DataFrame()
place_coord = pd.read_csv('place_zone_coordinates.csv')
place_coord


# In[83]:


place_coord_point_zero = place_coord[place_coord['point_number'] == 0]
place_coord_point_zero


# In[84]:


place_coord['loc_lat_lead'] = place_coord.groupby(['place_id'])['loc_lat'].shift(-1)
place_coord['loc_lon_lead'] = place_coord.groupby(['place_id'])['loc_lon'].shift(-1)
place_coord


# In[85]:


place_coord_dataset = pd.merge(place_coord, place_coord_point_zero, 'left', 'place_id')
place_coord_dataset


# In[86]:


import math

for i in range(len(place_coord_dataset)):
    if math.isnan(place_coord_dataset.loc[i, 'loc_lat_lead']) == True and math.isnan(place_coord_dataset.loc[i, 'loc_lon_lead']) == True:
        place_coord_dataset.loc[i, 'loc_lat_lead'] = place_coord_dataset.loc[i, 'loc_lat_y']
        place_coord_dataset.loc[i, 'loc_lon_lead'] = place_coord_dataset.loc[i, 'loc_lon_y']
place_coord_dataset   


# In[87]:


place_coord_dataset = place_coord_dataset.drop(columns = ['loc_lat_y', 'loc_lon_y', 'point_number_y'])
place_coord_dataset


# In[88]:


x = data['point'][0]
y = data['point'][1]
for i in range(len(data['polygon'])):
    xp = data['polygon'][i][0]
    yp = data['polygon'][i][1]
    xp_prev = data['polygon'][i-1][0]
    yp_prev = data['polygon'][i-1][1]
    if (((yp <= y and y < yp_prev) or (yp_prev <= y and y < yp)) and (x > (xp_prev - xp) * (y - yp) / (yp_prev - yp) + xp)):
        in_polygon = not in_polygon


# In[89]:


place_coord_dataset['key'] = 0
user_coord['key'] = 0

dataset = pd.merge(user_coord, place_coord_dataset, 'outer', 'key')
dataset


# In[91]:



dataset['trig'] = np.where((((dataset['loc_lon_x'] <= dataset['loc_lon']) & (dataset['loc_lon'] < dataset['loc_lon_lead']) 
   | (dataset['loc_lon_x'] > dataset['loc_lon']) & (dataset['loc_lon'] >= dataset['loc_lon_lead'])) 
  & (dataset['loc_lat'] > (dataset['loc_lat_x'] - dataset['loc_lat_lead']) * 
     (dataset['loc_lon'] - dataset['loc_lon_lead']) / (dataset['loc_lon_x'] - dataset['loc_lon_lead']) + dataset['loc_lat_lead'])), 1, 0)
dataset



# In[92]:


new_data = dataset.groupby(by = ['place_id', 'user_id']).agg({'trig': 'sum'}).reset_index()
new_data


# In[93]:


new_data = new_data[new_data['trig'] % 2 == 1]
final_table = new_data.groupby(by = 'user_id').agg({'trig': 'size'})
final_table

