# Importing the basic libraries
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from PIL import Image
import urllib.request
import matplotlib.pyplot as plt


#Starting streamlit codes
def page_layout():
    st.set_page_config(
        page_title = "City Search Tool",
        layout = "wide",
        initial_sidebar_state = "expanded"
    )
    # Header for a webpage
    st.write("""
    # City Search Tool for Millenials
    
    This web app helps in finding the appropriate city to move into based on the user preferences
    """)
    city_image_url = r"https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1113&h=450&q=80"
    image = Image.open(urllib.request.urlopen(city_image_url))
    st.image(image, use_column_width=True)
    st.markdown("""Photo by [Pedro Lastra](https://unsplash.com/@peterlaster?utm_source=unsplash&amp;utm_medium=referral&amp;utm_content=creditCopyText)
        on [Unsplash](https://unsplash.com/s/photos/city?utm_source=unsplash&amp;utm_medium=referral&amp;utm_content=creditCopyText)""")

    with st.beta_expander(label="Information about calculation", expanded=False):
        st.markdown("""[Nestpick](https://www.nestpick.com/millennial-city-ranking-2018/) studied thousands of cities focusing on capitals,\
         economic and ex-pat hubs to determine \
         the top 100 millennial dream destinations. Following feedback about the importance of education to this generation,\
          they added 10 more locations to better cover major university cities. From looking deeper into what millennials \
          care about, they also adjusted the weightings of each category to reflect this, for instance Essentials \
          (housing, internet, university etc) accounts for a higher percentage than Recreation (nightlife, beer price etc.)\
          
        **Scoring**: In order to standardize the results and create a comprehensive score, all of the different factors have been \
        evenly ranked between 0 and 10. A score of 10 indicates the highest possible score, while 0 is the lowest possible. \
        This score is obtained directly from the raw data and implementing a normalization of the form:\
        
        **Score(i) = 10 . ( ( (x(i) - x(min) ) / ( (x(max) - x(min) ) )**
     """)

    st.write("----")
    st.sidebar.header('Input Level of Importance') #Creating header for the sidebar
    return

page_layout()

#Importing the required Dataset
def data_import():
    #url = r"C:\Users\nilaya\Desktop\ML Model Start to Deployment\CityTool\Millennial Cities Ranking by Indicator with coordinates.csv"
    url = r"https://github.com/nepalbinay/ML_with_Deployment/blob/master/CityTool/Millennial%20Cities%20Ranking%20by%20Indicator%20with%20coordinates.csv?raw=True"
    df_orig = pd.read_csv(url)
    df = df_orig.drop(['Unnamed: 0','Overall Score'], axis = 1)
    column_names = df.columns[0:17]
    return df, column_names

df, column_names = data_import()

parameter_options = ['Not Important','Little Important','Important','Very Important'] #Options to display in slider

#Selecting only interested paramters

def multi_select(options):
    return column_names if 'All' in options else options


def column_display(col_display):
    col_display.insert(0,'All')
    list(col_display).remove('City')
    return col_display

col_to_display = list(column_names)
col_to_display.remove("City")
col_to_display.insert(0,'All')

st.markdown('What factors concerns you?')
selected_parameters_tmp = st.multiselect("", col_to_display)
selected_parameters_tmp.insert(0,'City')
selected_parameters = multi_select(selected_parameters_tmp)

#function block to convert categorical value to numerical value
def string_to_value(value):
    if value == 'Very Important':
        return 10
    elif value == 'Important':
        return 5
    elif value == 'Little Important':
        return 1
    else:
        return 0

#Preparing the default values for the weights
initial_weights = dict((item,0) for item in column_names[1:])

# Loop to create parameter field and parameter_option selection
for i in range(len(selected_parameters)):
    parameter_name = selected_parameters[i]
    if parameter_name != 'City':
        parameter_value =  st.sidebar.selectbox(parameter_name, parameter_options)
    else:
        continue
    initial_weights[parameter_name] = string_to_value(parameter_value)

#Function to calculate total weighted score
def total_function(data,weights):
    data['Weighted Score'] = np.nan
    for i in range(data.shape[0]):
        total = 0
        for j in column_names[1:]:
            sub_total = 0
            dict_value = weights.get(j)
            cell_value = data.loc[i,j]
            sub_total = dict_value*cell_value
            total = total + sub_total
        data.loc[i,'Weighted Score'] = total
    return data

df_to_display = total_function(df,initial_weights).sort_values(by = ['Weighted Score'], ascending = False)
all_columns = df_to_display.columns
selected_parameters_tmp2 = list(selected_parameters)
selected_parameters_tmp2.insert(0,'Weighted Score')
new_columns_order = selected_parameters_tmp2


st.write("----")


t = st.slider('Number of Cities to Display in the table', 1, int(df_to_display.shape[0]), value=5)
st.markdown("Top "+ str(t) +" Cities based on your criteria")
st.table(df_to_display[new_columns_order].set_index('City').head(t).style.format('{:.2f}'))


def showing_map():
    fig = px.scatter_mapbox(df_to_display[:t], lat='lat',lon='lon',color='Weighted Score', hover_name='City', \
                            size='Weighted Score', zoom=1,height=600, \
                            center={'lat':32,'lon':34},width=1200)

    fig.update_layout(mapbox_style="open-street-map")

    st.plotly_chart(fig,use_container_width=False,sharing='streamlit')
    return

showing_map()



