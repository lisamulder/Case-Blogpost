#!/usr/bin/env python
# coding: utf-8

# # Case 2: Corona en vaccinatie wereld

# Namen: Fleur Molenaar, Lisa Mulder, Timon van Leeuwen en Sylvére Gumbs

# Studentnummers: 500802473, 500831854, 500782708, 500747086

# # 1 System setup

# In[1]:


#pip install streamlit


# In[2]:


# Importeren van packages
import requests
import pandas as pd
from pandas import json_normalize
import json
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# Stream-lit

# In[3]:


st.title('Case 2 corona en vaccinatie over de wereld')


# In[4]:


st.markdown('Wij hebben een API gekozen over coronabesmettingen over de hele wereld en de vaccinatiegraad.')


# In[5]:


st.header('1 Systeem opzetten')


# In[6]:


st.write('Alle packages installeren en inladen.')


# # 2 Import van de data 

# In[7]:


st.header('2 Importeren van de data')


# In[8]:


st.write('We hebben twee api gebruikt over de corona besmettingen en de vaccinaties.')


# In[9]:


# Inladen van API's. url1 is de API omtrent de besmettingen en url2 de vaccinaties.
url1 = 'https://covid-api.mmediagroup.fr/v1/cases'
url2 = 'https://covid-api.mmediagroup.fr/v1/vaccines'
r1 = requests.get(url1)
r2 = requests.get(url2)


# In[10]:


#Variabelen maken voor de text van de response van de twee GET requests.
json_string1 = r1.text
json_string2 = r2.text


# # 3 Data verkennen

# In[11]:


st.header('3 Data verkennen')


# # 3.1 Dataframes maken

# In[12]:


st.subheader('3.1 Dataframes maken')


# In[13]:


st.write('Vervolgens hebben we van de api omgezet naar dataframes en die dataframes hebben we samengevoegd.')


# In[14]:


#JSon strings van de twee URL's omzetten naar een dictionary format.
dict1 = json.loads(json_string1)
dict2 = json.loads(json_string2)


# In[15]:


#Eerste dictionary(dict1) omzetten naar een dataframe en vervolgens alle niet-NaN waarden voor kolom 'country' tonen.
df1 = pd.concat({k: pd.DataFrame(v).T for k, v in dict1.items()})
df1 = df1[df1['country'].notna()]


# In[16]:


#Tweede dictionary(dict2) omzetten naar een dataframe en vervolgens alle niet-NaN waarden voor kolom 'country' tonen.
df2 = pd.concat({k: pd.DataFrame(v).T for k, v in dict2.items()})
df2 = df2[df2['country'].notna()]


# In[17]:


#Controleer dataset1(besmettingen) voor meer NaN waarden.
df1.isna().sum()


# In[18]:


#Controleer dataset2(vaccinaties) voor meer NaN waarden
df2.isna().sum()


# In[19]:


#Shape van dataset1(besmettingen)
st.write('Shape van de eerste dataset over coronagevallen.')
df1.shape


# In[20]:


#Shape van dataset2(vaccinaties)
st.write('Shape van de tweede dataset over de vaccinaties.')
df2.shape


# In[21]:


#Dataset1 en dataset2 samenvoegen op basis van gelijke kolommen. Nu hebben we één dataset met aantal besmettingen en gevaccineerden.
df = df1.merge(df2, on=['abbreviation', 'capital_city', 'continent', 'country', 'elevation_in_meters', 'iso',                        'life_expectancy', 'location', 'population', 'sq_km_area'])


# In[22]:


#Shape van dataset1(besmettingen) en dataset2(vaccinaties) samengevoegd.
st.markdown('Shape van de twee datasets samengevoegd over de  coronagevallen en vaccinaties.')
df.shape


# # 3.2 Kolommen verwijderen

# In[23]:


st.subheader('3.2 Kolommen verwijderen')


# In[24]:


st.write('We hebben kolommen die we niet gaan gebruiken verwijderd.')


# In[25]:


# Kolommen verwijderen die we niet gaan gebruiken
df.drop('elevation_in_meters', axis = 1, inplace = True)
df.drop('iso', axis = 1, inplace = True)
df.drop('lat', axis = 1, inplace = True)
df.drop('location', axis = 1, inplace = True)
df.drop('long', axis = 1, inplace = True)
df.drop('recovered', axis = 1, inplace = True)
df.drop('updated_x', axis = 1, inplace = True)
df.drop('updated_y', axis = 1, inplace = True)


# In[26]:


#Alleen de niet-NaN waarden weergeven in de kolom 'continent'.
df = df[df['continent'].notna()]


# In[27]:


#dataframe weergeven na alle aanpassingen
st.markdown('Dataframe nadat de kolommen zijn verwijderd.')
st.write(df.head())


# # 3.3 Kolommen samenvoegen/toevoegen

# In[28]:


st.subheader('3.3 Kommen samenvoegen/toevoegen')


# In[29]:


st.write('We hebben een aantal kolommen toevoegd om nieuwe variabelen te creëren. Hieronder zijn de toegevoegde kolommen te zien.')


# In[30]:


#Kolom toevoegen aan dataset van percentage overledenen per aantal besmette.
df['%_deaths'] = (df['deaths'] * 100) / df['confirmed']
#Kolom toevoegen aan dataset van de percentage van de aantal gevacineerden per populatie van elk land
df['%_vaccinated'] = (df['people_vaccinated'] * 100) / df['population']
#Kolom toevoegen aan dataset van de percentage van de aantal corona gevallen per populatie van elk land
df['%_confirmed'] = (df['confirmed'] * 100) / df['population']


# In[31]:


df_pluskolommen = df[['country','%_deaths', '%_vaccinated', '%_confirmed']]


# In[55]:


st.write(df_pluskolommen.set_index('country').head())


# # 4 Visualisatie van de data

# In[33]:


st.header('4 Visualisatie van de data')


# # 4.1 Histogram

# In[34]:


st.subheader('4.1 Histogram percentage overledenen per aantal besmette')


# In[35]:


st.write('We hebben een histogram gemaakt die toont de waardes van de kolom percentage van de overledenen per totaalbesmette mensen. Wat wel opvalt is dat de histogram lijkt op een normale verdeling. Verder zien we dat veel mensen die besmetraakte een best wel hoge kans heeft om de ziekte te overleven(>97%).')


# In[56]:


# Histogram maken van de percentage van de aantal overledenen per aantal besmette.
fig1 = px.histogram(data_frame=df, x='%_deaths',
                   title = 'Histogram percentage overledenen per aantal besmette personen',
                   labels = {'%_deaths':'Percentage overledenen per aantal besmette personen',
                            })
fig1.update_layout(yaxis_title = 'Aantal')
#fig1.show()


# In[37]:


st.plotly_chart(fig1)


# # 4.2 Spreidingsdiagrammen..

# In[38]:


st.subheader('4.2 Percentage coronadoden en vaccinatiegraad per land')


# In[39]:


st.write('We maken een spreidingsdiagram van het percentage gevaccineerde inwoners per land en het percentage inwoners dat is overleden aan corona. Met behulp van een dropdown menu kan je inzoomen op de gegevens van één continent. Er is te zien dat veel landen in Afrika een lage vaccinatiegraad hebben, namelijk minder dan 15%. Ook lijkt er een zwak negatief verband te zijn tussen de variabelen. In veel gevallen gaat een hoge vaccinatiegraad gepaard met een laag percentage coronadoden.')


# In[40]:


# Create figure
fig2 = go.Figure()

continents = ['Asia', 'Europe', 'Africa', 'North America', 'South America', 'Oceania']

# Scatterplots met for loop
for x in continents:
    fig2.add_trace(go.Scatter(x=df[df["continent"]==x]['%_deaths'],
                             y=df[df["continent"]==x]['%_vaccinated'],
                             name=x,
                             mode='markers'
                            ))

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
fig2.update_layout(title="Percentage coronadoden en vaccinatiegraad per land",
                  xaxis_title='Coronadoden per besmetting (%)',
                  yaxis_title='Vaccinatiegraad (%)',
                  legend_title='Continent')

# Dropdown toevoegen
fig2.update_layout({
    'updatemenus':[{
        'type':'dropdown',
        'x':1.3, 'y':0.4,
        'showactive':True,
        'active':0,
        'buttons':dropdown_buttons}]
    })

#fig2.show()


# In[41]:


st.plotly_chart(fig2)


# # 4.3 Staafdiagram en spreidingsdiagram..

# In[42]:


st.subheader('4.3 Levensverwachting per land')


# In[43]:


st.write('We maken een staafdiagram van de levensverwachting per land. Aan de kleuren van de landen is te zien bij welk continent ze horen. Met behulp van een knopje kan de staafdiagram omgezet worden in een spreidingsdiagram en andersom. In het spreidingsdiagram is goed te zien dat veel Afrikaanse landen en een paar Aziatische landen een lage levensverwachting hebben, namelijk maximaal 60 jaar.')


# In[44]:


# Levensverwachting omzetten naar een decimaal getal.
df['life_expectancy'] = df['life_expectancy'].astype(float)


# In[45]:


# Figuur maken
fig3 = px.bar(
    data_frame=df,
    x='country', y='life_expectancy',
    color='continent'
)

# Buttons maken
buttons = [
    {'label':'Staafdiagram', 'method':'update', 'args':[{'type':'bar'}]},
    {'label':'Spreidingsdiagram', 'method':'update', 'args':[{'type':'scatter', 'mode':'markers'}]}
]

# Opmaak van de grafiek
fig3.update_layout(title="Levensverwachting per land",
                  xaxis_title='Land',
                  yaxis_title='Levensverwachting',
                  legend_title='Continent')

# Buttons toevoegen
fig3.update_layout({'updatemenus':[{'type':'buttons',
                                    'direction':'down',
                                    'x':1.3, 'y':0.3,
                                    'showactive':True,
                                    'active':0,
                                    'buttons':buttons}]})

#fig3.show()


# In[46]:


st.plotly_chart(fig3)


# # 4.4 Spreidingsdiagrammen..

# In[47]:


st.subheader('4.4 Spreidingsdiagram van het percentage besmette mensen tegen land oppervlakte')


# In[48]:


st.write('Dit is een spreidingsdiagram met een slider op de x-as. We zien hier de oppervlakte van het land op de x-as en het percentage van het aantal besmette mensen op de y-as. Met de slider onder het figuur kan je inzoomen op het gedeelte dat je wilt zien. Verder heeft elk continent een eigen kleur.')


# In[49]:


#Spreidingsdiagrammen met een 'slidebar' ...
fig4 = px.scatter(data_frame=df, 
                  x='sq_km_area', 
                  y='%_confirmed', 
                  color='continent', 
                  hover_name='country')

fig4.update_layout(
    title={'text': 'Spreidingsdiagram van het percentage besmette mensen tegen land oppervlakte', 'x':0.46, 'y':0.92},
    yaxis= {'title':{'text': 'Besmette mensen in populatie (%)'}},
    legend_title='Continenten',
    xaxis=dict(
        title='Land oppervlakte (km^2)',
        range=[0,17500000],
        rangeslider=dict(
            range=[0,17500000],
            visible=True)
    )
)

#fig4.show()


# In[50]:


st.plotly_chart(fig4)


# In[51]:


st.subheader('4.5 Spreidingsdiagram van het percentage gevaccineerde mensen tegen land oppervlakte')


# In[52]:


st.write('Dit is een spreidingsdiagram met een slider op de x-as. We zien hier de oppervlakte van het land op de x-as en het percentage van het aantal gevaccineerde mensen op de y-as. Met de slider onder het figuur kan je inzoomen op het gedeelte dat je wilt zien. Verder heeft elk continent een eigen kleur.')


# In[53]:


fig5 = px.scatter(data_frame=df, 
                  x='sq_km_area', 
                  y='%_vaccinated', 
                  color='continent', 
                  hover_name='country')

fig5.update_layout(
    title={'text': 'Spreidingsdiagram van het percentage gevaccineerde mensen tegen land oppervlakte', 'x':0.46, 'y':0.92},
    yaxis= {'title':{'text': 'Gevaccineerde mensen in populatie (%)'}},
    legend_title='Continenten',
    xaxis=dict(
        title='Land oppervlakte (km^2)',
        range=[0,17500000],
        rangeslider=dict(
            range=[0,17500000],
            visible=True)
    )
)

#fig5.show()


# In[54]:


st.plotly_chart(fig5)

