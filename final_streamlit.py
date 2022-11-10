# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 10:38:53 2022

@author: luuk
"""

import pandas as pd
import numpy as np
import plotly.express as px
import warnings
import plotly.graph_objects as go
import streamlit as st
from pandas.core.common import SettingWithCopyWarning

warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

df = pd.read_csv("cause_of_deaths.csv")

col_list = df.columns.values.tolist()

#col_list.remove('Country/Territory')
col_list.remove('Code')
col_list.remove('Year')

df['total'] = df[col_list].sum(axis=1)

populatie = pd.read_csv("populatie.csv")

populatie.drop(['Series Name', 'Series Code'], axis=1, inplace=True)

column_list = populatie.columns.tolist()
id_vars_list = column_list[:2] + column_list[-1:]

populatie2 = pd.melt(populatie, id_vars=id_vars_list, 
             value_name="year").drop(['variable'],axis=1).sort_values('year')

populatie_jaren = populatie[['1990 [YR1990]', '1991 [YR1991]',
       '1992 [YR1992]', '1993 [YR1993]', '1994 [YR1994]', '1995 [YR1995]',
       '1996 [YR1996]', '1997 [YR1997]', '1998 [YR1998]', '1999 [YR1999]',
       '2000 [YR2000]', '2001 [YR2001]', '2002 [YR2002]', '2003 [YR2003]',
       '2004 [YR2004]', '2005 [YR2005]', '2006 [YR2006]', '2007 [YR2007]',
       '2008 [YR2008]', '2009 [YR2009]', '2010 [YR2010]', '2011 [YR2011]',
       '2012 [YR2012]', '2013 [YR2013]', '2014 [YR2014]', '2015 [YR2015]',
       '2016 [YR2016]', '2017 [YR2017]', '2018 [YR2018]', '2019 [YR2019]',
       '2020 [YR2020]', '2021 [YR2021]']]

populatie2 = pd.melt(populatie, id_vars=['Country Name', 'Country Code'], value_vars=['1990 [YR1990]', '1991 [YR1991]',
       '1992 [YR1992]', '1993 [YR1993]', '1994 [YR1994]', '1995 [YR1995]',
       '1996 [YR1996]', '1997 [YR1997]', '1998 [YR1998]', '1999 [YR1999]',
       '2000 [YR2000]', '2001 [YR2001]', '2002 [YR2002]', '2003 [YR2003]',
       '2004 [YR2004]', '2005 [YR2005]', '2006 [YR2006]', '2007 [YR2007]',
       '2008 [YR2008]', '2009 [YR2009]', '2010 [YR2010]', '2011 [YR2011]',
       '2012 [YR2012]', '2013 [YR2013]', '2014 [YR2014]', '2015 [YR2015]',
       '2016 [YR2016]', '2017 [YR2017]', '2018 [YR2018]', '2019 [YR2019]',
       '2020 [YR2020]', '2021 [YR2021]'], var_name='Year', value_name='populatie')


populatie2["Year"].replace(r"\D+", "", regex=True, inplace=True)

populatie2['Year'] = [x[:4] for x in populatie2['Year']]

populatie2["Year"] = populatie2["Year"].astype(int)

populatie2['populatie'] = populatie2['populatie'].str.strip()

populatie2["populatie"] = populatie2['populatie'].str.replace(r'\D', '')

populatie2["populatie"] = populatie2['populatie'].replace('', np.nan)

populatie2.dropna(subset=['populatie'], inplace=True)

populatie2['populatie']= populatie2['populatie'].astype(float)
populatie2['populatie']= populatie2['populatie'].astype(int)

df2 = df.merge(populatie2, how='left', left_on=['Code', 'Year'], right_on=['Country Code', 'Year'])

list_of_columns = ['Meningitis',
       "Alzheimer's Disease and Other Dementias", "Parkinson's Disease",
       'Nutritional Deficiencies', 'Malaria', 'Drowning',
       'Interpersonal Violence', 'Maternal Disorders', 'HIV/AIDS',
       'Drug Use Disorders', 'Tuberculosis', 'Cardiovascular Diseases',
       'Lower Respiratory Infections', 'Neonatal Disorders',
       'Alcohol Use Disorders', 'Self-harm', 'Exposure to Forces of Nature',
       'Diarrheal Diseases', 'Environmental Heat and Cold Exposure',
       'Neoplasms', 'Conflict and Terrorism', 'Diabetes Mellitus',
       'Chronic Kidney Disease', 'Poisonings', 'Protein-Energy Malnutrition',
       'Road Injuries', 'Chronic Respiratory Diseases',
       'Cirrhosis and Other Chronic Liver Diseases', 'Digestive Diseases',
       'Fire, Heat, and Hot Substances', 'Acute Hepatitis']

def ziekte_per_aantal(df, list_of_columns):
    new_df = pd.DataFrame()
    new_df[['Country/Territory', 'Code', 'Year', 'populatie']] = df[['Country/Territory', 'Code', 'Year', 'populatie']]
    for i in range(len(list_of_columns)):
        new_name = list_of_columns[i] + " per 100k"
        new_df[new_name] = df[list_of_columns[i]]/df['populatie']*100000
        
    return new_df


df_100k = ziekte_per_aantal(df2, list_of_columns)

fig_scatter_1 = px.scatter(df2, x="populatie", y="Meningitis", color = "Country/Territory", trendline = "ols")
fig_scatter_1.update_layout(showlegend=False)

fig_scatter_2 = px.scatter(df2, x="Year", y="Meningitis", color = "Country/Territory", trendline = "ols")
fig_scatter_2.update_layout(showlegend=False)

fig_per100k_1 = px.scatter(df_100k, x="populatie", y="Meningitis per 100k", color = "Country/Territory", trendline = "ols")
fig_per100k_1.update_layout(showlegend=False)


fig_per100k_2 = px.scatter(df_100k, x="Year", y="Meningitis per 100k", color = "Country/Territory", trendline = "ols")
fig_per100k_2.update_layout(showlegend=False)

df_100k_diseases = df_100k.drop(columns=['Code', 'Year'], axis=1)
data = pd.DataFrame(df_100k_diseases.groupby(['Country/Territory'])['Meningitis per 100k'].sum().sort_values(ascending =False)[:5]).reset_index()

fig_per100k_3 = px.bar(data ,x = 'Country/Territory' , y='Meningitis per 100k', color='Country/Territory')
fig_per100k_3.update_layout(title=go.layout.Title(text="COUNTRIES WITH HIGHEST Meningitis per 100k DEATHS"))
fig_per100k_3.update_xaxes(tickangle=45)


##############################################################################################################
##############################################################################################################
##############################STREAMLIT#######################################################################
##############################################################################################################
##############################################################################################################
st.set_page_config(layout="wide")

#Achtergrond streamlit
def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url(https://wallpaperaccess.com/full/1454447.jpg);
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url() 

from streamlit_option_menu import option_menu


# 2. horizontal menu
selected2 = option_menu(None, ["Home", "Kaart", "Aantal doden per ziekte", "Vergelijkingen"], 
    icons=['house', 'map', "reception-3", 'arrow-left-right'], 
    menu_icon="cast", default_index=0, orientation="horizontal")

if selected2 == 'Home':
    country = st.sidebar.selectbox('Country' ,(df2['Country/Territory'].unique()))

    st.header("**Oorzaken van overlijden wereldwijd over de jaren heen**")
    st.markdown("Luuk en Maxim")


    st.plotly_chart(fig_per100k_3)

   
elif selected2 == 'Kaart':
    col1, col2 = st.columns(2)


        
    disease = st.sidebar.selectbox('Kies een doodoorzaak' , (list_of_columns))

    fig_choropleth_1 = px.choropleth(df2, locations="Code",
                        animation_frame="Year",
                        color=disease, 
                        hover_name="Country/Territory", 
                        color_continuous_scale=px.colors.sequential.Plasma)
    
    fig_choropleth_3 = px.choropleth(df_100k, locations="Code",
                        animation_frame="Year",
                        color= disease + " per 100k", 
                        hover_name="Country/Territory", 
                        color_continuous_scale=px.colors.sequential.Plasma)   

    with col1:
        st.plotly_chart(fig_choropleth_1)
    with col2:
        st.plotly_chart(fig_choropleth_3)

elif selected2 == 'Aantal doden per ziekte':
    disease_2 = st.sidebar.selectbox('Kies een doodoorzaak' , (list_of_columns))

    fig_1 = px.histogram(df2, x=disease_2, nbins=20)

    fig_2 = px.box(df2, x=disease_2)

    fig_3 = px.strip(df2,
             x=disease_2,
             color='Country/Territory',
             stripmode='overlay')
    fig_3.add_trace(go.Box(y=df.query('Meningitis == "trace 0"')['Meningitis'], name='trace 0'))
    fig_3.update_layout(showlegend=False)
    
    st.plotly_chart(fig_1)
    st.plotly_chart(fig_2)
    st.plotly_chart(fig_3) 
    st.plotly_chart(fig_scatter_1)
    st.plotly_chart(fig_per100k_1)

    st.plotly_chart(fig_scatter_2)
    st.plotly_chart(fig_per100k_2)

elif selected2 == 'Vergelijkingen':
    col1, col2 = st.columns(2)

    country = st.sidebar.selectbox('Selecteer een land' ,(df2['Country/Territory'].unique()))
    vergelijken_aan = st.sidebar.checkbox('Ik wil vergelijken')
    
    country_data = df2.loc[df2['Country/Territory'] == country]
    fig_per_country = px.bar(country_data, x = "Year" , y="Meningitis", color="Country/Territory")
    fig_scatter_3 = px.scatter(country_data, x = "populatie" , y="Meningitis", color = "Country/Territory", trendline = "ols")
    fig_scatter_4 = px.scatter(country_data, x = "Year" , y="Meningitis", color = "Country/Territory", trendline = "ols")
    country_data_100k = df_100k.loc[df_100k['Country/Territory'] == country]
    fig_per100k_5 = px.scatter(country_data_100k, x = "Year" , y="Conflict and Terrorism per 100k", color = "Country/Territory", trendline = "ols")
    
    if vergelijken_aan:
 
        country_2 = st.sidebar.selectbox('Selecteer een tweede land' ,(df2['Country/Territory'].unique()))

        country_data_2 = df2.loc[df2['Country/Territory'] == country_2]
        fig_per_country_2 = px.bar(country_data_2, x = "Year" , y="Meningitis", color="Country/Territory")
        fig_scatter_3_2 = px.scatter(country_data_2, x = "populatie" , y="Meningitis", color = "Country/Territory", trendline = "ols")
        fig_scatter_4_2 = px.scatter(country_data_2, x = "Year" , y="Meningitis", color = "Country/Territory", trendline = "ols")
        country_data_100k_2 = df_100k.loc[df_100k['Country/Territory'] == country_2]
        fig_per100k_5_2 = px.scatter(country_data_100k_2, x = "Year" , y="Conflict and Terrorism per 100k", color = "Country/Territory", trendline = "ols")
        
        with col1:
            st.plotly_chart(fig_scatter_3)
            st.plotly_chart(fig_scatter_4)
            st.plotly_chart(fig_per_country)
            st.plotly_chart(fig_per100k_5)
    
        with col2:
            st.plotly_chart(fig_scatter_3_2)
            st.plotly_chart(fig_scatter_4_2)
            st.plotly_chart(fig_per_country_2)
            st.plotly_chart(fig_per100k_5_2)
    else:     
        with col1:
            st.plotly_chart(fig_scatter_3)
            st.plotly_chart(fig_scatter_4)

        with col2:
            st.plotly_chart(fig_per_country)
            st.plotly_chart(fig_per100k_5)

