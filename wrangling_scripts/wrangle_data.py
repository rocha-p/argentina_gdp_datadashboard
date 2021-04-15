import pandas as pd
import plotly.graph_objs as go
import requests
import numpy as np
from collections import defaultdict


#List of countries
countrylist = ['Argentina', 'Brazil','Latin America & Caribbean','Uruguay']

# get from the World Bank API: GDP growth (annual %) data for Brazil, Argentina, Uruguay and Latin America
payload = {'format': 'json', 'per_page': '500', 'date':'1970:2020'}
r = requests.get('http://api.worldbank.org/v2/countries/ar;br;uy;zj/indicators/NY.GDP.MKTP.KD.ZG', params=payload)
#Create a dictionary for the data
gdp = defaultdict(list)
for entry in r.json()[1]:
    # check if country is already in dictionary. If so, append the new x and y values to the lists
    if gdp[entry['country']['value']]:
        gdp[entry['country']['value']][0].append(float(entry['value']))       
    else: # if country not in dictionary, then initialize the lists that will hold the x and y values
        gdp[entry['country']['value']] = [[]]
        
#Create a Data frame
df_gdp = pd.DataFrame(columns=gdp.keys())
#Create a years column and set as index
df_gdp['Years'] = np.arange(2019,1969,-1)
df_gdp.set_index('Years', inplace=True)

#Fill the DF with the values for each country
for country in df_gdp:
    df_gdp[country] = gdp[country][0]
    
#Sort the values
df_gdp.reset_index(inplace=True)
df_gdp.sort_values('Years' ,inplace=True)


# get the World Bank GDP Per Capita data for Brazil, Argentina, Uruguay and Latin America
payload = {'format': 'json', 'per_page': '500', 'date':'1970:2020'}
r = requests.get('http://api.worldbank.org/v2/countries/ar;br;uy;zj/indicators/NY.GNP.PCAP.CD', params=payload)
#Create a dict for the data
gdp_pc = defaultdict(list)

for entry in r.json()[1]:
    # check if country is already in dictionary. If so, append the new x and y values to the lists
    if gdp_pc[entry['country']['value']]:
        gdp_pc[entry['country']['value']][0].append(float(entry['value']))       
    else: # if country not in dictionary, then initialize the lists that will hold the x and y values
        gdp_pc[entry['country']['value']] = [[]]
        
#Create a DataFrame        
df_gdp_pc = pd.DataFrame(columns=gdp_pc.keys())
#Create a column for Years 
df_gdp_pc['Years'] = np.arange(2019,1969,-1)
df_gdp_pc.set_index('Years', inplace=True)

#Fill the DF with the values for each country
for country in df_gdp_pc:
    df_gdp_pc[country] = gdp_pc[country][0]
    
#Sort the values
df_gdp_pc.reset_index(inplace=True)
df_gdp_pc.sort_values('Years' ,inplace=True)


def return_figures():
    """Creates two plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the two plotly visualizations

    """

    # first chart plots 
    # as a line chart GDP growth (annual %)
    graph_one = []
    for country in countrylist:
        x_val = df_gdp['Years'].tolist()
        y_val =  df_gdp[country].tolist()
        graph_one.append(
          go.Scatter(
          x = x_val,
          y = y_val,
          mode = 'lines',
          name = country))
    
    layout_one = dict(title = 'GDP growth (annual %)',
                xaxis = dict(title = 'Year'),
                yaxis = dict(title = '%'),
                )

# second chart plots GDP per capita (current U$D)
    graph_two = []
    for country in countrylist:
        x_val = df_gdp_pc['Years'].tolist()
        y_val =  df_gdp_pc[country].tolist()
        graph_two.append(
          go.Scatter(
          x = x_val,
          y = y_val,
          mode = 'lines',
          name = country))
    
    layout_two = dict(title = 'GDP per Capita (current U$D)',
                xaxis = dict(title = 'Year'),
                yaxis = dict(title = 'U$S'),
                )

 
    # append all charts to the figures list
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))

    return figures