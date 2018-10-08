
# coding: utf-8

# In[228]:


# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import time
import json

# Import API key
from api_keys import api_key


# Incorporated citipy to determine city based on latitude and longitude
from citipy import citipy

# Output File (CSV)
output_data_file = "output_data/cities.csv"

# Range of latitudes and longitudes
lat_range = (-90, 90)
lng_range = (-180, 180)


# In[229]:


# List for holding lat_lngs and cities
lat_lngs = []
cities = []

# Create a set of random lat and lng combinations
lats = np.random.uniform(low=-90.000, high=90.000, size=1500)
lngs = np.random.uniform(low=-180.000, high=180.000, size=1500)
# lat_lngs = zip(lats, lngs)

#*************************************
coordinates = list(zip(lats, lngs))
cities = []
countries = []

for coordinate_pair in coordinates:
    lat, lon = coordinate_pair
    city = citipy.nearest_city(lat, lon).city_name
    country = citipy.nearest_city(lat, lon).country_code
    cities.append(city)
    countries.append(country)
Cities_data = pd.DataFrame({"City": cities, "Country":countries})  

# Drop any duplicate values
Cities_data = Cities_data.drop_duplicates('City')

# Visualize the data frame
Cities_data.head()


# ## Generate Cities List

# In[230]:


# create a DataFrame
Cities_data["Lat"] = ""
Cities_data["Lon"] = ""
Cities_data["Date"] = ""
Cities_data["Humidity"] = ""
Cities_data["Temperature"] = ""
Cities_data["Cloudiness"] = ""
Cities_data["Wind"] = ""

Cities_data.head()


# ## Perform API Calls

# In[234]:


# Loop through the list of cities and add the data to the df.
url = "http://api.openweathermap.org/data/2.5/weather?" #appid=?
api_key = "eff2eb5e4734b95ca01b0f266dab22f3"
row_count = 1


print("Beginning Data Retrieval")
for index, row in Cities_data.iterrows():
    target_city = row["City"]
    target_url = url + "appid=" + api_key + "&units=IMPERIAL" + "&q=" + target_city.replace(" ","+")
    print(target_url)
    city_data = requests.get(target_url).json()
    if city_data["cod"] == "404":
        print("City not found, skipping...")

    else:
        #clean_cities_df.set_value(index, "City", city_data["name"])
        
        Cities_data.set_value(index, "Temperature (F)", city_data["main"]["temp"])
        Cities_data.set_value(index, "Latitude", city_data["coord"]["lat"])
        Cities_data.set_value(index, "Longitude", city_data["coord"]["lon"])
        Cities_data.set_value(index, "Humidity (%)", city_data["main"]["humidity"])
        Cities_data.set_value(index, "Cloudiness (%)", city_data["clouds"]["all"])
        Cities_data.set_value(index, "Wind Speed (mph)", city_data["wind"]["speed"])
        
        print("------------------------")
        print("Proceesing: City # " , row_count, ' | ' , city_data["name"], city_data["sys"]["country"])
        print(target_url)
        row_count += 1

