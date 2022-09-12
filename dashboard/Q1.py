import pickle

import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title='Canonical Assignment',
    layout='wide'
)

st.subheader('Q1: Have wildfires become more or less frequent over time?')

col1, _, col3 = st.columns(3)

with open('assets/fires_by_year.pickle', 'rb') as f:
    fires_by_year = pickle.load(f)

fig = px.line(fires_by_year, x='fire_year', y='counts')
# col1.line_chart(fires_by_year)
col1.plotly_chart(fig)
col1.caption('You can hover on the line chart to see more details.')

col3.write(fires_by_year)

st.markdown('As we can see from the chart above, the forest fire rate was quite turbelent from 1992 to 1996; when it reached its lowest recorded point in 1997.Then it steadily\
    rose to 2000 when it dipped again all the way to 2003. Then experiencing its biggest recorded rise in 2006. The rate experienced some turbelence when it finally settled in\
        2015 at 74,491 fires that year.')
