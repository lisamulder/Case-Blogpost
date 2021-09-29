#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install streamlit


# In[2]:


import requests
import pandas as pd
from pandas import json_normalize
import json
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# In[3]:


url1 = 'https://covid-api.mmediagroup.fr/v1/cases'
url2 = 'https://covid-api.mmediagroup.fr/v1/vaccines'
r1 = requests.get(url1)
r2 = requests.get(url2)


# In[4]:


json_string1 = r1.text
json_string2 = r2.text


# In[5]:


dict1 = json.loads(json_string1)
dict2 = json.loads(json_string2)


# In[6]:


df1 = pd.concat({k: pd.DataFrame(v).T for k, v in dict1.items()})
df1 = df1[df1['country'].notna()]


# In[7]:


df2 = pd.concat({k: pd.DataFrame(v).T for k, v in dict2.items()})
df2 = df2[df2['country'].notna()]


# In[8]:


df1.isna().sum()


# In[9]:


df2.isna().sum()


# In[10]:


df1.shape


# In[11]:


df2.shape


# In[12]:


df = df1.merge(df2, on=['abbreviation', 'capital_city', 'continent', 'country', 'elevation_in_meters', 'iso', 'life_expectancy', 'location', 'population', 'sq_km_area'])


# In[13]:


# Kolommen verwijderen die we niet gaan gebruiken
df.drop('elevation_in_meters', axis = 1, inplace = True)
df.drop('iso', axis = 1, inplace = True)
df.drop('lat', axis = 1, inplace = True)
df.drop('location', axis = 1, inplace = True)
df.drop('long', axis = 1, inplace = True)
df.drop('recovered', axis = 1, inplace = True)
df.drop('updated_x', axis = 1, inplace = True)
df.drop('updated_y', axis = 1, inplace = True)


# In[14]:


df = df[df['continent'].notna()]


# In[15]:


df['deaths_confirmed'] = (df['deaths'] * 100) / df['confirmed']
df['people_vaccinated_population'] = (df['people_vaccinated'] * 100) / df['population']
df['people_confirmed_population'] = (df['confirmed'] * 100) / df['population']


# In[16]:


# Histogram maken
fig1 = px.histogram(data_frame=df, x='deaths_confirmed')
fig1.show()


# In[17]:


# Histogram maken
fig2 = px.histogram(data_frame=df, x='people_vaccinated_population')
fig2.show()


# In[18]:


# Scatterplot maken
fig3 = px.scatter(data_frame=df, x='deaths_confirmed', y='administered', color='continent')
fig3.show()


# In[19]:


# Create figure
fig4 = go.Figure()

continents = ['Asia', 'Europe', 'Africa', 'North America', 'South America', 'Oceania']

# Scatterplots met for loop
n = 0
for x in continents:
    fig4.add_trace(go.Scatter(x=df[df["continent"]==x]['deaths_confirmed'],
                             y=df[df["continent"]==x]['people_vaccinated_population'],
                             name=x,
                             mode='markers'
                            ))
    n += 1

# Dropdown maken
dropdown_buttons = [
    {'label':'Alle continenten', 'method':'update', 'args':[{'visible':[True, True, True, True, True, True]}, {'title':'Relatieve coronadoden en vaccinatiegraad per land'}]},
    {'label':'Azië', 'method':'update', 'args':[{'visible':[True, False, False, False, False, False]}, {'title':'Relatieve coronadoden en vaccinatiegraad in Azië'}]},
    {'label':'Europa', 'method':'update', 'args':[{'visible':[False, True, False, False, False, False]}, {'title':'Relatieve coronadoden en vaccinatiegraad in Europa'}]},
    {'label':'Afrika', 'method':'update', 'args':[{'visible':[False, False, True, False, False, False]}, {'title':'Relatieve coronadoden en vaccinatiegraad in Afrika'}]},
    {'label':'Noord-Amerika', 'method':'update', 'args':[{'visible':[False, False, False, True, False, False]}, {'title':'Relatieve coronadoden en vaccinatiegraad in Noord-Amerika'}]},
    {'label':'Zuid-Amerika', 'method':'update', 'args':[{'visible':[False, False, False, False, True, False]}, {'title':'Relatieve coronadoden en vaccinatiegraad in Zuid-Amerika'}]},
    {'label':'Oceanië', 'method':'update', 'args':[{'visible':[False, False, False, False, False, True]}, {'title':'Relatieve coronadoden en vaccinatiegraad in Oceanië'}]},
]

# Opmaak van de grafiek
fig4.update_layout(title="Relatieve coronadoden en vaccinatiegraad per land",
                  xaxis_title='Coronadoden per besmetting',
                  yaxis_title='Vaccinatiegraad',
                  legend_title='Continent')

fig4.update_layout({
    'updatemenus':[{
        'type':'dropdown',
        'x':1.2, 'y':0.5,
        'showactive':True,
        'active':0,
        'buttons':dropdown_buttons}]
    })

fig4.show()


# In[20]:


df.continent.unique()


# In[21]:


df['life_expectancy'] = df['life_expectancy'].astype(float)


# In[22]:


fig5 = px.bar(
    data_frame=df,
    x='country', y='life_expectancy',
    color='continent'
)
fig5.show()


# In[23]:


st.plotly_chart(fig5)


# In[24]:


df.dtypes


# In[25]:


fig6 = px.scatter(data_frame=df, 
                  x='sq_km_area', 
                  y='people_confirmed_population', 
                  color='continent', 
                  hover_name='country')

fig6.update_layout(
    title={'text': 'Scatterplot percentage infected people vs area size', 'x':0.47, 'y':0.92},
    yaxis= {'title':{'text': 'Percentage infected of population (%)'}},
    legend_title='Continents',
    xaxis=dict(
        title='Area (km^2)',
        range=[0,17500000],
        rangeslider=dict(
            range=[0,17500000],
            visible=True)
    )
)

fig6.show()


# In[26]:


fig7 = px.scatter(data_frame=df, 
                  x='sq_km_area', 
                  y='people_vaccinated_population', 
                  color='continent', 
                  hover_name='country')

fig7.update_layout(
    title={'text': 'Scatterplot percentage vaccinated people vs area size', 'x':0.47, 'y':0.92},
    yaxis= {'title':{'text': 'Percentage vaccinated of population (%)'}},
    legend_title='Continents',
    xaxis=dict(
        title='Area (km^2)',
        range=[0,17500000],
        rangeslider=dict(
            range=[0,17500000],
            visible=True)
    )
)

fig7.show()


# In[ ]:




