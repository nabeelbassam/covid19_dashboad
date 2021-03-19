# Nabeel Ayyad
# 122162
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(
    layout="centered",
    initial_sidebar_state="collapsed",
    page_title='Covid-19 Dashboard',
    page_icon=None,
)

# using requests library to deal with corona api
url_request = requests.get("https://corona-api.com/countries")
url_json = url_request.json()
df = pd.DataFrame(url_json['data'])

# preprocessing
# extract latitude and longitude from coordinates columns
# extract deaths and confirmed, recovered, critical from latest_data columns
# extract today_deaths and today_confirmed from today columns

latitude = []
longitude = []
deaths = []
confirmed = []
recovered = []
critical = []
today_deaths = []
today_confirmed = []
for i in df.index:
    latitude.append(df['coordinates'][i]['latitude'])
    longitude.append(df['coordinates'][i]['longitude'])
    deaths.append(df['latest_data'][i]['deaths'])
    confirmed.append(df['latest_data'][i]['confirmed'])
    recovered.append(df['latest_data'][i]['recovered'])
    critical.append(df['latest_data'][i]['critical'])
    today_deaths.append(df['today'][i]['deaths'])
    today_confirmed.append(df['today'][i]['confirmed'])

df['latitude'] = latitude
df['longitude'] = longitude
df['deaths'] = deaths
df['confirmed'] = confirmed
df['recovered'] = recovered
df['critical'] = critical
df['today_deaths'] = today_deaths
df['today_confirmed'] = today_confirmed
df = df.drop('coordinates', axis=1)
df = df.drop('today', axis=1)
df = df.drop('latest_data', axis=1)

# set title and markdown for the Dashboard
st.title("Covid-19 Dashboard")
st.markdown('The dashboard will visualize the Covid-19 Situation')
st.markdown('Coronavirus disease (COVID-19) is an infectious '
            'disease caused by a newly discovered coronavirus, '
            'The best way to prevent and slow down transmission is to be well informed about '
            'the COVID-19 virus, the disease it causes and how it spreads. Protect yourself'
            ' and others from infection by washing your hands or using an alcohol based rub'
            ' frequently and not touching your face.')

# Set a title of sidebar
st.sidebar.title("Visualization Selector")

# set a checkbox for showing data as a table
if st.sidebar.checkbox("Show Data ", False, key=1):
    st.dataframe(
        df[['name', 'population', 'deaths', 'confirmed', 'recovered',
            'critical', 'today_deaths', 'today_confirmed']],
        width=800, height=500)

# show analysis by country with 2 selectors one for input country
# and another for select plot type 
if st.sidebar.checkbox("Show Analysis by country", False, key=2):

    select = st.sidebar.selectbox('Select a country', df.name)
    # get the country selected in the selectbox
    select_values = df[df.name == select][['deaths', 'confirmed',
                                           'recovered', 'critical']].values.flatten()
    select2 = st.sidebar.selectbox('Visualization type',
                                   ['Bar plot', 'Pie chart'], key='5')
    if select2 == 'Pie chart':
        fig = px.pie(df, values=select_values,
                     names=['deaths', 'confirmed', 'recovered', 'critical'],
                     title='covid-19 patients status in ' + select, width=700, height=500)
        st.plotly_chart(fig)

    if select2 == 'Bar plot':
        country_graph = px.bar(
            select_values,
            color=['deaths', 'confirmed', 'recovered', 'critical'],
            text=['deaths', 'confirmed', 'recovered', 'critical'],
            title='covid-19 patients status in ' + select,
            orientation='h'
        )
        st.plotly_chart(country_graph)

# get selected status from radio list
select_status = st.sidebar.radio("Covid-19 patient's status on a map", ('deaths', 'confirmed',
                                                                        'recovered', 'critical'))

# build choropleth map to display countries
fig2 = px.choropleth(df, locations='name', color=select_status,
                     color_continuous_scale='Reds',scope = "world",
                     locationmode = 'country names'
                     )
fig2.update_layout(title_text='Global spread of Covid19')
st.plotly_chart(fig2)

# display top 10 effected countries using scatter plot
top10_select_status = df[['name', select_status]]. \
    sort_values(by=select_status, ascending=False).nlargest(10, select_status)

fig1 = px.scatter(top10_select_status, x=top10_select_status.name,
                  y=select_status, size=select_status, size_max=120,
                  color=top10_select_status.name, title='Top 10 ' + select_status + ' Cases Countries')
st.plotly_chart(fig1)

top_countries = df.nlargest(5, select_status)
# display top 5 effected countries using stack bar plot
fig6 = go.Figure(data=[
    go.Bar(name='Recovered Cases', x=top_countries['name'], y=top_countries['recovered']),
    go.Bar(name='Active Cases', x=top_countries['name'], y=top_countries['confirmed']),
    go.Bar(name='Critical Cases', x=top_countries['name'], y=top_countries['critical']),
    go.Bar(name='Death Cases', x=top_countries['name'], y=top_countries['deaths'])

])
fig6.update_layout(title='Most Affected countries', barmode='stack', height=600)
st.plotly_chart(fig6)

fig, ax = plt.subplots(1, 1)

