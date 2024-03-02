
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path


# Load the dataset
file_path = Path(__file__).parents[1] / "cleaning/cleaned_data/cleaned_time_series_all.csv"
nps_info_path = Path(__file__).parents[1] / "cleaning/cleaned_data/cleaned_nps_info.csv"
data = pd.read_csv(file_path)
data.head()

# 1. Visualize yearly changes in the number of visitors and expenditures:
def visualize_yearly_trends(data):
    """
    Visualizes yearly trends in national park visitation and spending.
    
    Args:
    - data: pandas DataFrame containing columns 'Year', 'Visitation', and 'Spending'.
    
    This function creates a dual-axis line chart with one axis for visitation 
    and the other for spending. 
    The visitation trend is shown in red, and the spending trend is shown in blue.
    
    Note: 
        Visitation Trend (Red Line): This line shows the changes in the number 
        of visitors to national parks from 2011 to 2022. 
        There appears to be a general upward trend in visitation, 
        suggesting an increasing interest in national parks. 
        This could be due to various factors, such as the rising popularity of 
        outdoor activities, improvements in park accessibility, 
        or enhanced awareness and promotion of national parks.
        
        Spending Trend (Blue Line): The blue line represents the changes in 
        spending within national parks over the same period. 
        Like the visitation trend, spending also shows an upward trajectory, 
        which likely correlates with the increase in visitors. 
        As more people visit the parks, the overall expenditure within the parks 
        increases, indicating that the parks are generating more revenue, 
        possibly from entry fees, concessions, and other services.
    """
    # Filtering the data for the years 2011-2022
    filtered_data = data[(data['Year'] >= 2011) & (data['Year'] <= 2022)]

    # Creating the visualization
    sns.set(style="whitegrid")
    fig, ax1 = plt.subplots(figsize=(14, 8))

    color = 'tab:red'
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Visitation', color=color)
    ax1.plot(filtered_data['Year'].unique(), 
             filtered_data.groupby('Year')['Visitation'].sum(), color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('Spending', color=color)
    ax2.plot(filtered_data['Year'].unique(), 
             filtered_data.groupby('Year')['Spending'].sum(), color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()
    plt.title('Yearly Trends in National Park Visitation and Spending (2011-2022)')
    plt.show()


# 2. Analyze the correlation between climate data and the number of visitors:
def analyze_correlation(data):
    """
    Analyzes the correlation between climate variables and visitation.
    
    Args:
    - data: pandas DataFrame containing visitation data and specified climate variables.
    
    This function calculates the correlation matrix for the specified climate 
    variables and visitation, and visualizes it using a heatmap.
    """
    # Specifying climate variables to analyze
    climate_variables = ['temp_avg', 'precip_sum', 'visibility', 'uvindex']
    
    # Calculating the correlation matrix
    correlation = data[climate_variables + ['Visitation']].corr()

    # Visualizing the correlation matrix using a heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation, annot=True, cmap='coolwarm', center=0)
    plt.title('Correlation between Climate Variables and Visitation')
    plt.show()
    

# 3. Compute and visualize the overall correlation:
def compute_and_visualize_correlation(data):
    """
    Computes and visualizes the correlation matrix for spending, visitation, 
    and climate variables.
    
    Args:
    - data: pandas DataFrame containing 'Spending', 'Visitation', and climate variables.
    
    This function first cleans the data by dropping NA values, 
    computes the correlation matrix, and then visualizes it using a heatmap.
    
    Note: The correlation matrix provides insights into the relationships 
    between different variables.
    """
    # Filtering the data for the years 2011-2022
    data_filtered = data[(data['Year'] >= 2011) & (data['Year'] <= 2022)]

    # Selecting relevant data for correlation analysis
    data_relevant = data_filtered[['Spending', 'Visitation', 'temp_avg', 'precip_sum', 
                                   'visibility', 'uvindex']].copy()

    # Clean data by dropping NA values and calculate the correlation matrix
    data_cleaned = data_relevant.dropna()
    correlation_matrix = data_cleaned.corr()

    # Visualizing the correlation matrix using a heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', 
                xticklabels=correlation_matrix.columns, 
                yticklabels=correlation_matrix.columns)
    plt.title('Correlation Matrix of Visitation, Spending, and Climate Variables (2011-2022)')
    plt.show()


# 4. Analyze the growth rate of each park:
def analyze_growth_rate(data):
    """
    Analyzes the growth rate of visitation for each park between 2011 and 2022
    and identifies the park with the highest and lowest average growth rate.
    
    Args:
    - data: pandas DataFrame containing 'Year', 'Park Name', and 'Visitation'.
    
    Returns:
    - A tuple containing the name of the top growing park, its average growth rate, 
    the name of the top declining park, and its average growth rate.
    """
    # Filtering the data for the years 2011-2022
    filtered_data = data[(data['Year'] >= 2011) & (data['Year'] <= 2022)]

    # Calculate the change (%) in visitation for each park by year
    visitation_growth = filtered_data.pivot_table(index='Year', columns='Park Name', 
                                                  values='Visitation').pct_change().mul(100)
    
    # Replace infinite values with NaN
    visitation_growth.replace([float('inf'), float('-inf')], np.nan, inplace=True)

    # Calculate the average growth rate for each park, excluding NaN values
    average_growth_rate = visitation_growth.mean().sort_values(ascending=False)

    # Identifying the top growing and declining parks
    top_growing_park = average_growth_rate.idxmax()
    top_declining_park = average_growth_rate.idxmin()

    return (top_growing_park, average_growth_rate[top_growing_park], 
            top_declining_park, average_growth_rate[top_declining_park])


# 5. Compare the COVID period (2020-2022) with the period before and after:
def compare_covid_period(data):
    """
    Compares visitation, spending, and climate variables before 
    and during the COVID-19 period (2020-2022).
    
    Args:
    - data: pandas DataFrame containing 'Year', 'Spending', 'Visitation', 
    and climate variables.
    
    Prints summary statistics for the COVID-19 period (2020-2022) 
    and the period before it, and returns the summaries as pandas DataFrames.
    
    Note: 
        Summary Analysis for 2020-2022:
        - Spending: In 2020, the average spending was $7,733.84.
                    It slightly increased to $7,907.29 in 2021.
                    In 2022, the average spending further rose to $8,049.65.
                    Observation: There's a gradual increase in spending 
                                  across these years.
        - Visitation: In 2020, the average visitation was 1,078,281.
                      There was a significant increase in 2021, 
                      with an average visitation of 1,464,315.
                      In 2022, the visitation slightly decreased to 1,407,336 
                      but was still higher than in 2020.
                      Observation: Visitation dipped in 2020, 
                                   likely due to the pandemic, 
                                   but showed a recovery in 2021 and 2022.
        - Temperature (temp_avg): The average temperature slightly decreased 
                                  from 53.32 in 2020 to 52.51 in 2022.
                                  Observation: Minor fluctuations in temperature 
                                  were observed, likely within normal climatic variation.
        - Precipitation (precip_sum): Precipitation was relatively stable in 2020 
                                      and 2021 but decreased in 2022.
                                      Observation: Precipitation showed a slight 
                                      decreasing trend in 2022.
        - Visibility: Increased from 9.70 in 2020 to 10.74 in 2022.
                      Observation: Improved visibility might indicate fewer 
                                   pollution sources or clearer weather conditions.
        - UV Index (uvindex): Slight upward trend from 6.39 in 2020 to 6.52 in 2022.
                              Observation: This could be due to seasonal variations 
                              or clearer skies.
        - Severe Risk (severerisk): No data for 2020 and 2021, but in 2022 
                                    the severe risk was recorded at 16.69.
                                    Observation: This new metric in 2022 suggests 
                                    an introduction or better recording of 
                                    environmental or weather-related risks.
        
        Comparison with the Period Before 2020: 
            When comparing the averages from 2020-2022 with those before 2020, 
            we see that spending increased slightly during the pandemic, 
            while visitation showed a more volatile pattern due to the initial 
            impact of COVID-19 and subsequent recovery.
            The climate variables (temperature, precipitation, visibility, and UV index) 
            don't show significant deviations from the pre-2020 averages, 
            indicating that these factors remained relatively stable despite the pandemic.
    """
    # Filtering data for 2020-2022
    data_2020_2022 = data[data['Year'].between(2020, 2022)]

    # Selecting specific columns for analysis
    columns_to_analyze = ['Spending', 'Visitation', 'temp_avg', 'precip_sum', 
                          'visibility', 'severerisk']
    summary_2020_2022 = data_2020_2022.groupby('Year')[columns_to_analyze].mean()

    # Data before 2020
    data_pre_2020 = data[data['Year'] < 2020]
    summary_pre_2020 = data_pre_2020.groupby('Year')[columns_to_analyze].mean().mean()

    # Ensure full display of the DataFrame in the output
    with pd.option_context('display.max_columns', None):
        print("Summary for 2020-2022 period:\n", summary_2020_2022)

    print("\nSummary for period before 2020:\n", summary_pre_2020)

    return summary_2020_2022, summary_pre_2020


# 6. Yearly visitation trend per State
def generate_state_visitation_plots(file_path, nps_info_path):
    """
    Generates and saves plots showing yearly difference in visitation for 
    parks in each state.

    Parameters:
    - time_series_path (str): The file path to the time series data.
    - nps_info_path (str): The file path to the NPS info data.
    """
    nps_info = pd.read_csv(nps_info_path)
    time_series_all = pd.read_csv(file_path)

    # Merge the datasets on 'Park Name'
    merged_data = pd.merge(time_series_all, nps_info[['Park Name', 'State']], 
                           on='Park Name', how='left')

    # Filter the data for the years 2011 to 2022
    filtered_data = merged_data[(merged_data['Year'] >= 2011) 
                                & (merged_data['Year'] <= 2022)]

    # Group the data by 'State', 'Park Name', and 'Year', and sum the visitation
    grouped_data = filtered_data.groupby(['State', 'Park Name', 'Year'])\
                    ['Visitation'].sum().reset_index()

    # Calculate the total visitation per state
    state_total_visitation = grouped_data.groupby(['State'])\
                            ['Visitation'].sum().reset_index()\
                            .sort_values(by='Visitation', ascending=False)

    # Get the sorted list of states
    sorted_states = state_total_visitation['State'].tolist()

    # Calculate the yearly difference in visitation for each park
    grouped_data['Yearly Difference'] = grouped_data.groupby(['State', 
                                        'Park Name'])['Visitation'].diff()

    for i in range(0, len(sorted_states), 3):
        fig, axes = plt.subplots(1, 3, figsize=(20, 6))
        
        states_in_plot = sorted_states[i:i+3]
        for j, state in enumerate(states_in_plot):
            if j >= len(axes):
                break
            ax = axes[j]
            state_data = grouped_data[grouped_data['State'] == state]
            sns.lineplot(ax=ax, data=state_data, x='Year', 
                         y='Yearly Difference', hue='Park Name', marker='o')
            ax.set_title(f'{state} (Total Visitation: \
            {state_total_visitation[state_total_visitation["State"] == state]\
            ["Visitation"].values[0]})')
            ax.set_ylabel('Yearly Difference in Visitation')
            ax.set_xlabel('Year')

        plt.tight_layout()
        plt.show()
