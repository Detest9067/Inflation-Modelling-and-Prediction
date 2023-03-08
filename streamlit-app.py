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

fig, ax = plt.subplots(figsize=(12,6))

ax.bar(sorted_df.head(10)['Country'], sorted_df.head(10)['mean_inflation'], color='green')
ax.bar(sorted_df.tail(10)['Country'], sorted_df.tail(10)['mean_inflation'], color='red')
ax.set_yscale('log')

ax.set_xlabel('Country')
ax.set_ylabel('Mean Inflation (log scale)')
ax.set_title('Top 10 and Bottom 10 Mean Inflation Rates')
plt.xticks(rotation=270)

st.plt.show()