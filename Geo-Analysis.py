
# coding: utf-8

# API key = AIzaSyBaExoC_xY6qKJ4TF3MkW78Hhidr32ZSzg

# In[1]:

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')
import os


# # Finding Lat and Long of Top Stations 

# In[2]:

station_df = pd.read_csv('Data/StationEntrances.csv')
station_df.head(3)


# In[3]:

"""change = station_df[(station_df['Line'] == '6 Avenue') &                     (station_df['Station_Name'] ==                      '34th St')].Station_Name.replace('34th St','34 St Herald Sq')

for index,name in change.iteritems():
    station_df.loc[index,'Station_Name'] = name"""


# In[4]:

"""#Figuring out regular expressions in station names
station_name = ['Grand Central','Union Sq','Times Sq', '34 St Herald Sq'] #Grand central, Atlantic Avenue, Columbus Circle
latitude = []
longitude = []
for name in station_name:
    latitude.append(station_df[station_df.Station_Name.str.contains('^'+name)].Station_Latitude.mean())
    longitude.append(station_df[station_df.Station_Name.str.contains('^'+name)].Station_Longitude.mean())"""


# In[5]:

top20_to_lat_long = {
 'GRDCNTRL42ST4567S': ('Grand Central-42nd St', 40.751776, -73.976848),
 '34STHERALDSQBDFMNQR' : ('34 St - Herald Sq', 40.749567, -73.98795),
 'TIMESSQ42ST1237ACENQRS': ('Times Square-42nd St', 40.754672, -73.986754),
 '14STUNIONSQ456LNQR': ('14 St - Union Sq', 40.735736, -73.990568),
 'FULTONST2345ACJZ': ('Fulton St', 40.710374, -74.007582),
 '34STPENNSTAACE': ('34 St - Penn Station', 40.752287, -73.993391),
 '42STPORTAUTH1237ACENQRS': ('42 St - Port Authority Bus Terminal', 40.757308, -73.989735),
 '59STCOLUMBUS1ABCD': ('59 St - Columbus Circle', 40.768296, -73.981736),
 '59ST456NQR': ('59 St', 40.762526,-73.967967),
 '86ST456': ('86 St', 40.779492, -73.955589),
 '4750STSROCKBDFM': ('47-50 Sts - Rockefeller Ctr', 40.758663, -73.981329),
 'FLUSHINGMAIN7': ('Flushing - Main St', 40.7596, -73.83003),
 '34STPENNSTA123ACE': ('34 St - Penn Station', 40.750373, -73.991057),
 'JKSNHTROOSVLT7EFMR': ('Jackson Hts - Roosevelt Av', 40.746644, -73.891338),
 '42STBRYANTPK7BDFM': ('42 St - Bryant Pk', 40.754222, -73.984569),
 'ATLAVBARCLAY2345BDNQR': ('Atlantic Av - Barclays Ctr', 40.683666, -73.97881),
 'CANALST6JNQRZ': ('Canal St', 40.718092, -73.999892 ),
 'LEXINGTONAV536EM': ('Lexington Av/53 St', 40.757552, -73.969055),
 '96ST123': ('96 St', 40.793919, -73.972323),
 '14ST123FLM': ('14 St', 40.737826, -74.000201),
}


# In[6]:

top20_df = pd.DataFrame(top20_to_lat_long).T
latitude = list(top20_df.loc[:,1])
longitude = list(top20_df.loc[:,2])


# # Finding Lat and Long of Top Earners

# In[7]:

income_df = pd.read_csv('Data/medianhouseholdincomecensustract.csv')
income_df.head(3)


# In[8]:

#Median Household Income more than 100k
rich_families = income_df[(income_df['MHI']>100000) &                          ((income_df['COUNTY'] == 'New York County')                           | (income_df['COUNTY'] == 'Kings County')                           | (income_df['COUNTY'] == 'Bronx County')                           | (income_df['COUNTY'] == 'Queens County'))]
rich_families.LOCALNAME.value_counts().head(10)


# In[9]:

rich_latitude = rich_families.INTPTLAT10
rich_longitude = rich_families.INTPTLON10


# # Finding Lat and Long of Top Givers

# In[10]:

irs_df = pd.read_excel('Data/IRS_SOI_NY_2014.csv')
irs_df = irs_df.ix[10:]
irs_df.head(7)


# In[11]:

#Cutting off deduction by only those in the $100k or more bracket
irs_df = irs_df[(irs_df['Size of adjusted gross income']=='$100,000 under $200,000')             | (irs_df['Size of adjusted gross income']=='$200,000 or more')]


# In[12]:

irs_df.rename(columns={'Total itemized deductions': 'Total Itemized Deductions Amount'},inplace=True)
irs_df.rename(columns={'Unnamed: 57': 'Amount of AGI'},inplace=True)


# In[13]:

itemized_deduction = irs_df.groupby('ZIP\ncode [1]')['Total Itemized Deductions Amount'].sum()
Amount_of_AGI = irs_df.groupby('ZIP\ncode [1]')['Amount of AGI'].sum()


# In[14]:

deduction_df = pd.concat([itemized_deduction, Amount_of_AGI], axis=1)


# In[15]:

ratio = np.true_divide(itemized_deduction,Amount_of_AGI)


# In[16]:

generous_ratio = ratio[ratio[:] > 0.01]


# In[17]:

generous_zip_codes = list(generous_ratio.index)


# In[18]:

zip_to_lat_long = pd.read_csv('Data/Zip_to_Lat_Lon.txt')


# In[19]:

generous_lat = []
generous_long = []
for zip_code in generous_zip_codes:
    generous_lat.append(zip_to_lat_long[zip_to_lat_long.ZIP == zip_code].LAT)
    generous_long.append(zip_to_lat_long[zip_to_lat_long.ZIP == zip_code].LNG)


# # Geo-Plotting 

# In[20]:

from bokeh.io import output_notebook, show
from bokeh.models import ( GMapPlot, GMapOptions, ColumnDataSource,                           Circle, DataRange1d, PanTool,                           WheelZoomTool, BoxSelectTool
)


# In[25]:

def geoplotting(latitude,longitude,title):
    output_notebook()

    map_options = GMapOptions(lat=40.764811, lng=-73.973347,                               map_type="roadmap", zoom=11)

    plot = GMapPlot(
        x_range=DataRange1d(), y_range=DataRange1d(), \
        map_options=map_options
    )
    
    plot.title.text = title

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



# In[26]:

geoplotting(latitude,longitude,"Top Stations")


# In[27]:

geoplotting(rich_latitude,rich_longitude,"Affluent Areas")


# In[28]:

geoplotting(generous_lat,generous_long, "The Generous (OR Tax hacking)")


# In[ ]:



