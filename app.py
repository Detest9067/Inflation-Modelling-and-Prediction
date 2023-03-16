import src
import streamlit as st
from PIL import Image
import streamlit.components.v1 as components
import codecs
import seaborn as sns
import numpy as np
import h2o

st.set_page_config(
    page_title="Inflationary Tales",
    page_icon="🫠",
    layout="wide",
    initial_sidebar_state="expanded",
)

#functions for the pages and respective content
def page1():
    st.title("Contextual Background")
    st.write("This is the page for the contextual background of the analysis.")

def page2():
    st.title("Inflation")
    st.write("Let's start by taking a look at inflation by country over the past 15 years. You can use the slider to select which year you would like to check.")
    
    #define path for file
    path = 'data/Global Dataset of Inflation.csv'
    inflation_df = src.read_csv_file(path)

    #clean the inflation df using function in src
    sorted_df = src.inflation_df(inflation_df)
    # create tabs
    tab1, tab2, tab3 =st.tabs(['By year 📅', 'Top/Bottom 10 📊', '2008-2022 avg 📈'])
    

    with tab1:
        #year slider for yearly cloropleth
        year = st.slider('Select a year', min_value=2008, max_value=2022, value=2022) 

        #yearly cloropleth
        fig3 = src.year_choropleth(sorted_df, year)
        st.plotly_chart(fig3)
    
    with tab2:
        #run the top/bottom 10 plot function
        fig = src.plot_mean_inflation(sorted_df)
        st.pyplot(fig)

    with tab3:
        #run cloropleth function
        fig2 = src.create_choropleth(sorted_df)
        st.plotly_chart(fig2)
   
def page3():
    

    st.title("Additional Important Metrics")
    st.write("This is the page for the analysis of other important metrics.")

    # define path for file
    path = 'data/tax-rates.csv'
    tax_df = src.read_csv_file(path)

    # clean tax rate csv
    mean_tax_df = src.clean_and_sort_tax_df(tax_df)


    tab1, tab2, tab3 = st.tabs(["Tax Rate 💰", "Excess Mortality 💀", "GHI Data 🌍"])

    with tab1:
         # year slider
        year = st.slider('Select a year', min_value=2008, max_value=2022, value=2022)
        fig1 = src.tax_choropleth(year, mean_tax_df)
        st.plotly_chart(fig1)

    with tab2:
        # read excess mortality data
        st.write("Now we're going to look at excess death rates in the 2020-2022 period")
        path2 = 'data/excess-mortality.csv'
        ed_df = src.read_csv_file(path2)

        # clean excess mortality data
        new_df = src.excess_death_df(ed_df)

        # select country toggler
        selected_country = st.selectbox('Select a country', new_df['country'])

        # plot excess death
        if selected_country:
            fig2 = src.excess_death_graph(new_df, selected_country)
            st.plotly_chart(fig2)

    with tab3:
        # read and plot GHI data
        path3 = 'data/GHI.csv'
        ghi_df = src.read_csv_file(path3)
        
        # plot GHI data here
        
        country_names = ghi_df['Country'].unique()
        selected_country = st.selectbox('Select a country', country_names)
        ghi_df_filtered = ghi_df[ghi_df['Country'] == selected_country]
        if selected_country:
            fig3 = src.ghi_plot(ghi_df_filtered, selected_country)
            st.plotly_chart(fig3)

def page4():
    st.title("Correlation Analysis")
    st.write("This is the page for the correlation analysis.")
   
    path = 'data/combined_data.csv'
    correlation_df = src.read_csv_file(path)

        
    col1, col2 = st.columns(2)

    with col1:
        header = st.header("Kendall Tau")
        image = Image.open("/home/graham/Documents/Ironhack/Final-Project/images/kt.png")
        st.image(image, caption="Kendal Tau Correlation", use_column_width=True)

    with col2:
        st.header("Pearson")
        image = Image.open("/home/graham/Documents/Ironhack/Final-Project/images/pearson.png")
        st.image(image, caption="Pearson Correlation", use_column_width=True)

def page5():
    st.header("Machine Learning Summary")
    with st.container():
        col1, col2 = st.columns(2)
        
        with col1:
            image = Image.open("/home/graham/Documents/Ironhack/Final-Project/images/feature.png")
            st.image(image, caption="Feature Importance", use_column_width=True)

        with col2:
            image2 = Image.open("/home/graham/Documents/Ironhack/Final-Project/images/residuals.png")
            st.image(image2, caption="Residuals", use_column_width=True)
    st.subheader('Predicted vs Actual Values')
    image3 = Image.open('/home/graham/Documents/Ironhack/Final-Project/images/AvP2.png')
    st.image(image3, caption="Model Perfomance", use_column_width=True)

def page6():
    st.header("Predictor")
    h2o.init()
    ghi = st.slider('GHI', min_value=0, max_value=100, step=1)
    tax_rate = st.slider('Tax Rate', min_value=0, max_value=50, step=1)
    excess_deaths = st.slider('Excess Deaths', min_value=0, max_value=1000, step=10)
    input_data = h2o.H2OFrame({'GHI': [ghi], 'Tax_Rate': [tax_rate], 'Excess_Deaths': [excess_deaths]})

    if st.button('Predict'):
        predicted_rate =src.predict_inflation_rate(ghi, tax_rate, excess_deaths)
        st.write(f'Predicted inflation rate: {predicted_rate:.2f}%')
        st.write(input_data)
        
pages = {
    "Contextual Background 📖": page1,
    "Inflation 💸": page2,
    "Other Important Metrics 🗃": page3,
    "Correlation Analysis 👀": page4,
    "Machine Learning 💻": page5,
    "Predictions": page6,
    }

page = st.sidebar.selectbox('Select a page', list(pages.keys()))
pages[page]()