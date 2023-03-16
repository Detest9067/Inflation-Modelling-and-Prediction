import pandas as pd
import chardet
import missingno as msno
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.express as px
import kaleido
import streamlit as st
import h2o


#import any csv
def read_csv_file(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())  # detect encoding of file
    df = pd.read_csv(file_path, encoding=result['encoding'])
    return df

#cleaning of inflation dataframe
def inflation_df(df):
    df = df.drop(df.loc[:, '1970':'2007'].columns, axis=1)
    drop_columns = df.filter(regex='Unnamed').columns
    df = df.drop(drop_columns, axis=1)

    df_filtered = df[df.apply(lambda row: "Headline Consumer Price Inflation" in row.values, axis=1)]
    df_filtered = df_filtered.dropna()
    df_filtered['mean_inflation'] = df_filtered.loc[:, '2008':'2022'].mean(axis=1)

    sorted_df = df_filtered.sort_values('mean_inflation', ascending=False)
    return sorted_df

#top 10 and bottom 10 inflation countries over time period
def plot_mean_inflation(sorted_df):
    fig, ax = plt.subplots(figsize=(12,6))

    ax.bar(sorted_df.head(10)['Country'], sorted_df.head(10)['mean_inflation'], color='green')
    ax.bar(sorted_df.tail(10)['Country'], sorted_df.tail(10)['mean_inflation'], color='red')
    ax.set_yscale('log')

    ax.set_xlabel('Country')
    ax.set_ylabel('Mean Inflation (log scale)')
    ax.set_title('Top 10 and Bottom 10 Mean Inflation Rates')
    plt.xticks(rotation=270)

    return fig

#cloropleth map of mean inflation over the time period
def create_choropleth(sorted_df):
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
        ),
        width=1200,
        height=800 
    )

    fig = go.Figure(data=data, layout=layout)
    return fig

#yearly interest rate cloropleth
def year_choropleth(sorted_df, year):
    data = go.Choropleth(
        locations=sorted_df['Country Code'],
        z=sorted_df[str(year)],
        text=sorted_df['Country'],
        colorscale='Viridis',
        zmin=-5, # set the minimum value of the scale
        zmax=20, # set the maximum value of the scale
        colorbar=dict(
            title='Inflation',
            tickvals=[-5, 0, 5, 10, 15, 20], # set the tick values of the color bar
            ticktext=['< -5', '0', '5', '10', '15', '> 20'] # set the tick text of the color bar
        )
    )

    layout = go.Layout(
        title=f'Inflation by Country in {year}',
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'
        ),
        width=1200,
        height=800 
    )

    fig = go.Figure(data=data, layout=layout)
    return fig

#cleaning tax dataframe
def clean_and_sort_tax_df(tax_df):
    
    tax_df = tax_df.drop(['Unnamed: 0', 'iso_2', 'continent'], axis=1)
    tax_df = tax_df.drop(columns=[col for col in tax_df.columns if col.isdigit() and 1980 <= int(col) <= 2007])
    tax_df = tax_df.dropna()
    tax_df['mean_tax_rate'] = tax_df.loc[:, '2008':'2022'].mean(axis=1)
    tax_df = tax_df.reset_index(drop=True).sort_values('mean_tax_rate', ascending=False)
    
    return tax_df

#tax rate cloropleth
def tax_choropleth(year, mean_tax_df):
    fig = go.Figure(
        go.Choropleth(
            locations=mean_tax_df['iso_3'],
            z=mean_tax_df[str(year)],
            text=mean_tax_df['country'],
            colorscale='Viridis',
            zmin=0,
            zmax=50,
            colorbar=dict(
                title='Tax Rate'
            )
        )
    )
    
    fig.update_layout(
        title=f"Tax Rates by Country in {year} (%)",
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'
        ),
        width=1200,
        height=800,
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=50,
            pad=4
        )
    )
    
    return fig

#cleaning excess death df to plot
def excess_death_df(ed_df):
    # Extract the year from the 'Day' column and create a new 'Year' column in the original dataframe
    ed_df['Year'] = pd.DatetimeIndex(ed_df['Day']).year

    # Group the dataframe by 'Entity', 'Code', and 'Year' and calculate the mean
    grouped_df = ed_df.groupby(['Entity', 'Code', 'Year']).mean().reset_index()

    # Pivot the 'grouped_df' dataframe to create a new dataframe with 'Entity', 'Code', '2020 avg', '2021 avg', '2022 avg' columns
    new_df = grouped_df.pivot(index=['Entity', 'Code'], columns='Year', values='p_proj_all_ages').reset_index()

    # Flatten the multi-level columns index to a single-level index
    new_df.columns = [f'{str(col[0])}_{str(col[1])}' if isinstance(col, tuple) and col[1] != '' else str(col) for col in new_df.columns]

    # Rename the columns to 'country', 'code', and 'year'
    new_df = new_df.rename(columns={'Entity': 'country', 'Code': 'code', 'Year': 'year'})

    # Drop the '2023' column, if it exists
    if '2023' in new_df.columns:
        new_df = new_df.drop(columns=['2023'])

    # Drop rows with missing values
    new_df = new_df.dropna()

    # Reset the index
    new_df = new_df.reset_index()

    # Drop the 'index' column
    if 'index' in new_df.columns:
        new_df = new_df.drop(columns=['index'])

    return new_df

#excess death plot
def excess_death_graph(new_df, selected_country):
    # Filter the dataframe to only include the selected country
    filtered_df = new_df[new_df['country'] == selected_country]

    # Melt the dataframe to convert the wide format to long format
    melted_df = pd.melt(filtered_df, id_vars=['country', 'code'], var_name='year', value_name='average_excess_deaths')

    # Create a line graph to show the trend over time for the selected country
    fig = px.line(melted_df, x='year', y='average_excess_deaths', title=f'Excess Deaths Trend Over Time for {selected_country}')


    # Set axis labels
    fig.update_xaxes(title='Year')
    fig.update_yaxes(title='Average Excess Deaths')
    fig.update_layout(xaxis_range=[2020, 2022])

    # Set the x-axis tick values to only show integer years
    fig.update_layout(xaxis=dict(tickmode='linear'))

    fig.update_layout(width=1200, height=800)

    # Return the plot as a figure object
    return fig

#ghi plot
def ghi_plot(ghi_df, selected_country):
    fig, ax = plt.subplots(figsize=(10, 6))
          
    ghi_df.plot(kind='line', x='Year', y='GHI', ax=ax)

    # Set axis labels and title
    ax.set_xlabel('Year')
    ax.set_ylabel('GHI')
    ax.set_title(f'Global Hunger Index for {selected_country}')
    ax.set_xticks([2021, 2022])
    ax.set_xticklabels(['2021', '2022'])    
    
    # Add legend outside the plot area
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    return fig

#predictor
def predict_inflation_rate(ghi, tax_rate, excess_deaths):
    h2o.init()
    model_path = "/home/graham/Documents/Ironhack/Final-Project/best_model.mojo"
    best_model = h2o.import_mojo(model_path)
    # Create a H2OFrame with user inputs
    input_data = h2o.H2OFrame({'GHI': [ghi], 'Tax_Rate': [tax_rate], 'Excess_Deaths': [excess_deaths]})
    # Make predictions using the best model
    pred = best_model.predict(input_data)
    # Return the predicted inflation rate
    return pred[0,'predict']