import pickle

import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title='Canonical Assignment',
    layout='wide'
)

st.subheader('Q2: What counties are the most and least fire-prone?')

col1, _, col3 = st.columns(3)

with open('assets/fires_by_county.pickle', 'rb') as f:
    fires_by_county = pickle.load(f)

count = st.slider('Select the number of counties you want to display', min_value=10, max_value=100, value=25, step=5)
shift = st.slider('Select the number of counties you want to shift the chart by', min_value=0, max_value=1877, value=0, step=20)

subset = fires_by_county.loc[shift:shift+count]

fig = px.bar(subset, x='county', y='counts')
col1.plotly_chart(fig)
col1.caption('You can hover on the bar chart to see more details.')

col3.write(subset)

st.markdown("Since this data is very dense, you have control of the above sliders.\
    The first is to control how many counties to display at a time, from 10 to 100.\
    The second slider gives you even more control on the chart, it's a shift slider. Meaning you get to control by\
    how many data points you want to shift the starting point of the chart by.\
    For example, the default settings are 25 for the count slider and 0 for the shift slider; meaning that you are\
    viewing the first 25 observations of the data. If you were to set the count slider to 50\
    and the shift slider to 200, you would be viewing the data starting from the 200th index to the 250th index.\
    Let's say we want to view the ver last 100 observations, we would then set the count slider to 100, and\
    the shift slider to the very max (since the total count of the data is 1977).")
