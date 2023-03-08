import streamlit as st
from PIL import Image
import streamlit.components.v1 as components
import codecs
import matplotlib.pyplot as plt
import plotly.graph_objs as go


st.set_page_config(
     page_title="The unseen effects of Inflation",
     page_icon="U+1F4B0",
     layout="wide",
     initial_sidebar_state="expanded",
)

data = go.Choropleth(
    locations=sorted_df['Country Code'],
    z=sorted_df['mean_inflation'],
    text=sorted_df['Country'],
    colorscale='Viridis',
    zmin=-5, # set the minimum value of the scale
    zmax=20, # set the maximum value of the scale
    colorbar=dict(
        title='Mean Inflation',
        tickvals=[-5, 0, 5, 10, 15, 20], # set the tick values of the color bar
        ticktext=['< -5', '0', '5', '10', '15', '> 20'] # set the tick text of the color bar
    )
)

layout = go.Layout(
    title='Mean Annual Inflation by Country 2008-2022(%)',
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    )
)

st.fig = go.Figure(data=data, layout=layout)
st.fig.show()