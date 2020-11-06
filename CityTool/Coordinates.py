# Importing the basic libraries
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
!pip install opencage
from opencage.geocoder import OpenCageGeocode

#Importing the required Dataset
df_orig = pd.read_excel(path)
col1_name = df_orig.columns[0]
df_orig = df_orig.rename(columns={col1_name:'City','Apple Store':'University'}) #Changing the column names wherever required

#Adding latitude and longitude for the city using api
key = #Your key here
geocoder = OpenCageGeocode(key)
lat = []
lng = []

for i in range(df_orig.shape[0]):
    query = df_orig.City[i]
    result = geocoder.geocode(query)
    lat.append(result[0]['geometery']['lat'])
    lng.append(results[0]['geometry']['lng'])

df_orig['lat'] = lat
df_orig['lon'] = lng

df = df_orig.drop(['Overall Score'], axis = 1)
