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
    tab1, tab2 = st.tabs(["Background", "Data"])
    with tab1:
        st.markdown("**Inflation is a force that has pretty serious power over our everyday lives. As such, the purpose of this project is to explore the nature of the relationships that potentially influence inflation in daily life.**")
        st.subheader("Research Question 1: What influence do outside factors have on Inflation?")
        st.markdown("**The other factors we'll be analyzing within the context of inflation are:**")
        st.markdown("-Corporate Tax Rate")
        st.markdown("-Global Hunger Index")
        st.markdown("-Excess Deaths")
        st.markdown("")
        st.markdown("")
        st.subheader("Research Question 2: Can we predict Inflation based off other metrics")
        st.markdown("**Once we've built a statistical model based off our data, we'll use it to make predictions about future inflation rates**")
        meme = Image.open("/home/graham/Documents/Ironhack/Final-Project/images/inflation.jpeg")
        st.image(meme, caption="Inflation in a nutshell", use_column_width=True)
    with tab2:
        st.subheader("Data Sources")
        inflation = "https://www.kaggle.com/datasets/belayethossainds/global-inflation-dataset-212-country-19702022"
        st.write("[Inflation](%s)" %inflation)
        tax = "https://taxfoundation.org/publications/corporate-tax-rates-around-the-world/"
        st.write("[Corporate Tax Rate](%s)" %tax)
        ghilink1 = "https://www.kaggle.com/datasets/whenamancodes/the-global-hunger-index"
        ghilink2 = "https://www.kaggle.com/datasets/faduregis/global-hunger-index-2022-datasets?select=GHI2022+scores.csv"
        st.markdown("[Global Hunger Index (Source 1)](%s)" %ghilink1)
        st.markdown("[Global Hunger Index (Source 2)](%s)" %ghilink2)
        edr = "https://ourworldindata.org/excess-mortality-covid"
        st.write("[Excess Deaths](%s)" %edr)
        st.subheader("Data Cleaning/Processing")
        st.write("Due to the fact that all of the data came in CSV format, it was a relatively simple matter of cutting out emptys, renaming columns, calculating means, etc...")
        st.write("The nature of this data required to complete this analysis, there are few countries that have data for all 4 metrics we are looking to analyze")
        st.write("Here's a look at our final processed dataset:")
        df = src.read_csv_file("/home/graham/Documents/Ironhack/Final-Project/data/combined_data.csv")
        st.dataframe(df)
        st.write("TR = Tax Rate, Inf = Inflation, ED = Excess Deaths, and GHI = Global Hunger Index")

def page2():
    st.title("Inflation")
    st.write("Let's start by taking a look at inflation by country over the past 15 years.")
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
        st.write("Note that the scale is logarithmic, due to the massive discrepancy between Top and Bottom 10")

    with tab3:
        #run cloropleth function
        fig2 = src.create_choropleth(sorted_df)
        st.plotly_chart(fig2)
   
def page3():
 
    st.title("Additional Important Metrics")
    st.write("On this page you can find analysis of the other metrics we'll be using to analyze Inflation.")

    # define path for file
    path = 'data/tax-rates.csv'
    tax_df = src.read_csv_file(path)

    # clean tax rate csv
    mean_tax_df = src.clean_and_sort_tax_df(tax_df)


    tab1, tab2, tab3 = st.tabs(["Tax Rate 💰", "Excess Mortality 💀", "GHI Data 🌍"])

    with tab1:
        st.subheader("In the interactive map below, you can filter through corporate tax rates around the world, for each year between 2008-2022")
        # year slider
        year = st.slider('Select a year', min_value=2008, max_value=2022, value=2022)
        fig1 = src.tax_choropleth(year, mean_tax_df)
        st.plotly_chart(fig1)

    with tab2:
        # read excess mortality data
        st.subheader("On this tab you can see excess death rates in the 2020-2022 period per country")
        st.markdown("**You may be wondering: What is excess deaths or excess mortality?**")
        st.write("Excess mortality is measured as the difference between the reported number of deaths in a given week or month (depending on the country) in 2020–2022 and an estimate of the expected deaths for that period had the COVID-19 pandemic not occurred.")
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
        st.subheader("On this tab you can see the Global Hunger Index score for 2021 and 2022 by country")
        st.markdown("**Global Hunger Index presents a multidimensional measure of national, regional, and global hunger by assigning a numerical score based on several aspects of hunger. A GHI score is calculated on a 100-point scale reflecting the severity of hunger, where 0 is the best possible score (no hunger) and 100 is the worst**")        # read and plot GHI data
        path3 = 'data/GHI.csv'
        ghi_df = src.read_csv_file(path3)
        st.subheader('Global Hunger Index by Country:')
        # plot GHI data here
        country_names = ghi_df['Country'].unique()
        selected_country = st.selectbox('Select a country', country_names)
        ghi_df_filtered = ghi_df[ghi_df['Country'] == selected_country]
        if selected_country:
            fig3 = src.ghi_plot(ghi_df_filtered, selected_country)
            st.plotly_chart(fig3)

def page4():
    st.header("Correlation Analysis")
    st.write("**In order to determine the relationship between inflation and the other factors, a correlation analysis was run, using both the pearson and kendall tau method**.")
   
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
    tab1, tab2 = st.tabs(['Modelling & Training', 'Model Performance'])
    with tab1:
        st.subheader('In order to be able to predict future data, we need to find an appropriate model:')
        st.markdown('**Considering the nature of the data we are working with, a regression is probably the best type of model**')
        st.markdown('-Linear Regression R^2 score: -0.8028201857368651')
        st.markdown('-Decision Tree R^2 score: -0.5942452712475599')
        st.markdown('-Random Forest R^2 score: -0.22820700709030017')
        st.markdown('**Now that we know Random Forest is producing the best score of these options, we can use the H2O Auto Machine learning library to improve it**')
        st.write('The first step is to run an H2O Random Forest Estimator')
        summary = Image.open("/home/graham/Documents/Ironhack/Final-Project/images/model_summary.png")
        st.image(summary, caption="Model Summary", use_column_width=True)

        img1 = Image.open("/home/graham/Documents/Ironhack/Final-Project/images/cvmetrics.png")
        st.image(img1, caption='CV Metrics', use_column_width=True)
        
        with st.container():
            col1, col2 = st.columns(2)
            
            with col1:
                st.write('After looking at all the cross validations, the program loops through the results to find the best fold')
                img2 = Image.open("/home/graham/Documents/Ironhack/Final-Project/images/bestfold.png")
                st.image(img2, caption="Best Fold", use_column_width=True)
            with col2:
                st.write('The scores for our best model (CV6)')
                img3 = Image.open("/home/graham/Documents/Ironhack/Final-Project/images/modelmetrics.png")
                st.image(img3, caption="Model Metrics", use_column_width=True)

    with tab2:
        st.subheader("Variable Weight and Residuals")
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
    tab1, tab2 = st.tabs(['Predicted Values', 'Predictor'])
    
    with tab1:
        st.subheader("Using our model, we can predict the expected inflation rate in 2023 for the countries in our dataset")
        path = '/home/graham/Documents/Ironhack/Final-Project/data/predicted.csv' 
        df = src.read_csv_file(path)
        fig = src.predicted_plot(df)
        st.plotly_chart(fig)
    with tab2:
        st.subheader("We can also use our model to predict inflation based on the values of the other metrics")
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
    "Background & Data 📖": page1,
    "Inflation 💸": page2,
    "Other Important Metrics 🗃": page3,
    "Correlation Analysis 👀": page4,
    "Machine Learning 💻": page5,
    "Predictions 🔍": page6,
    }

page = st.sidebar.selectbox('Select a page', list(pages.keys()))
pages[page]()