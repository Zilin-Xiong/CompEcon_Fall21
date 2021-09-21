#!/usr/bin/env python
# coding: utf-8

# Assignment 3

# In[2]:


# imports
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.io as pio
# pio.renderers.default = 'jupyterlab'
pio.renderers.default = 'notebook' 
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[3]:


# Read in data from Excel 

firedata = pd.read_csv (r'C:\Users\PC\Desktop\forestfires.csv')


# In[4]:


# Take a look at the first 11 lines of data.
firedata.head(n=12)


# In[5]:


# Draw a scallter plot
scplot1 = plt.scatter(firedata['ISI'], firedata['wind'], alpha=0.2)
plt.ylabel('wind')
plt.xlabel('ISI')
plt.title('wind and ISI')


# In[8]:


## see if there exists a normal distribution for temp
import seaborn as sns
plt.style.use('ggplot') # select a style (theme) for plot
sns.distplot(firedata[firedata['temp'] > 0]['temp'], kde=True, rug=False)
plt.title('Distribution of Forest Temperature')
plt.xlabel('Temperature')


# In[6]:





# In[6]:


## Another 3D graph for rain, temp and wind
get_ipython().run_line_magic('matplotlib', 'notebook')
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection ='3d')
ax.scatter(firedata['temp'], firedata['wind'],
           firedata['RH'], c='r', marker='o')
ax.view_init(elev=50., azim=15)  # to rotate plot for better view
ax.set_xlabel('temp')
ax.set_ylabel('wind')
ax.set_zlabel('RH')
plt.title("the Relationship of Temperature, Wind, and Relative Humidity")
plt.show()


# In[9]:


# lineplot
staying_probs = (firedata['temp'])
# range 1 to 100 for centile
x = range(1, len(staying_probs) + 1)
# plotly express will want things in dataframe, so put back x and transmat in df
df = pd.DataFrame({"temp": staying_probs, "range": x})
# simple plot
px.line(df, x='range', y='temp')


# In[ ]:



