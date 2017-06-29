
# coding: utf-8

# API key = AIzaSyBaExoC_xY6qKJ4TF3MkW78Hhidr32ZSzg

# In[1]:

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')
import os


# ## Finding Lat and Long of Top Stations 

# In[2]:

station_df = pd.read_csv('Data/StationEntrances.csv')


# In[3]:

station_df.head(3)


# In[5]:

#Figuring out regular expressions in station names
station_name = ['Grand Central', 'Atlantic', '59th'] #Grand central, Atlantic Avenue, Columbus Circle
latitude = []
longitude = []
for name in station_name:
    latitude.append(station_df[station_df.Station_Name.str.contains('^'+name)].Station_Latitude.mean())
    longitude.append(station_df[station_df.Station_Name.str.contains('^'+name)].Station_Longitude.mean())


# ## Finding Lat and Long of Top Demographics 

# In[ ]:

#Matching CensusTrack to Lat/Long?


# ## Geo-Plotting 

# In[6]:

from bokeh.io import output_notebook, show
from bokeh.models import ( GMapPlot, GMapOptions, ColumnDataSource,                           Circle, DataRange1d, PanTool,                           WheelZoomTool, BoxSelectTool
)


# In[7]:

def geoplotting(latitude,longitude):
    output_notebook()

    map_options = GMapOptions(lat=40.764811, lng=-73.973347,                               map_type="roadmap", zoom=11)

    plot = GMapPlot(
        x_range=DataRange1d(), y_range=DataRange1d(), \
        map_options=map_options
    )
    
    plot.title.text = "New York City"

    plot.api_key = "AIzaSyBaExoC_xY6qKJ4TF3MkW78Hhidr32ZSzg"

    source = ColumnDataSource(
        data=dict(
            lat=latitude, #needs to be a list of latitude
            lon=longitude, #needs to be a corresponding list of long
        )
    )

    circle = Circle(x="lon", y="lat", size=15, fill_color="blue", fill_alpha=0.8, line_color=None)
    plot.add_glyph(source, circle)

    plot.add_tools(PanTool(), WheelZoomTool(), BoxSelectTool())
    show(plot)



# In[8]:

geoplotting(latitude,longitude)


# In[ ]:



