import streamlit as st
import pandas as pd
from PIL import Image
import streamlit.components.v1 as components
import codecs
import plotly.graph_objs as go


st.set_page_config(
     page_title="The unseen effects of Inflation",
     page_icon="U+1F4B0",
     layout="wide",
     initial_sidebar_state="expanded",
)
path = 'data/Global Dataset of Inflation.csv'
inflation_df = pd.read_csv_file(path)

#code for the overview of inflation
layout = go.Layout(
    title='Mean Annual Inflation by Country 2008-2022(%)',
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    )
)

# Define the initial data for the map
data = go.Choropleth(
    locations=df['Country Code'],
    z=df['mean_inflation'],
    text=df['Country'],
    colorscale='Viridis',
    zmin=-5, # set the minimum value of the scale
    zmax=20, # set the maximum value of the scale
    colorbar=dict(
        title='Mean Inflation',
        tickvals=[-5, 0, 5, 10, 15, 20], # set the tick values of the color bar
        ticktext=['< -5', '0', '5', '10', '15', '> 20'] # set the tick text of the color bar
    )
)

# Define the slider widget for the years
year = st.slider("Select a year", 2008, 2022)

# Filter the data based on the selected year
filtered_data = df[df["Year"] == year]

# Update the data for the map based on the selected year
data.locations = filtered_data['Country Code']
data.z = filtered_data['mean_inflation']
data.text = filtered_data['Country']

# Create the figure using Plotly
fig = go.Figure(data=data, layout=layout)

# Display the map
st.plotly_chart(fig)