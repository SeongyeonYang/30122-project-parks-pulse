
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the dataset
file_path = r'~/30122-project-parks-pulse/ppp/cleaned_data/cleaned_time_series_all.csv'
data = pd.read_csv(file_path)
data.head()

# 1. Visualize yearly changes in the number of visitors and expenditures:
def visualize_yearly_trends(data):
    """
    Visualizes yearly trends in national park visitation and spending.
    
    Parameters:
    - data: pandas DataFrame containing columns 'Year', 'Visitation', and 'Spending'.
    
    This function creates a dual-axis line chart with one axis for visitation and the other for spending. 
    The visitation trend is shown in red, and the spending trend is shown in blue.
    
    Note: Visitation trends generally show an upward trajectory, 
        indicating growing interest in national parks, possibly due to 
        increased outdoor activity popularity, park accessibility improvements, or heightened awareness. 
        However, a notable decrease was observed during 2022-2023, likely attributed to the COVID-19 pandemic. 
        Similarly, spending trends have also increased, 
        suggesting heightened economic activity from tourism, benefiting local areas and the parks themselves.
    """
    # Setting the style for seaborn plots
    sns.set(style="whitegrid")

    # Creating a figure and a single subplot
    fig, ax1 = plt.subplots(figsize=(14, 8))

    # Plotting visitation trends on the first y-axis
    color = 'tab:red'
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Visitation', color=color)
    ax1.plot(data['Year'].unique(), data.groupby('Year')['Visitation'].sum(), color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    # Creating a second y-axis to plot spending trends
    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('Spending', color=color)  
    ax2.plot(data['Year'].unique(), data.groupby('Year')['Spending'].sum(), color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    
    # Adjust layout to make room for the second y-axis and set the title
    fig.tight_layout()
    plt.title('Yearly Trends in National Park Visitation and Spending')
    plt.show()


# 2. Analyze the correlation between climate data and the number of visitors:
def analyze_correlation(data):
    """
    Analyzes the correlation between climate variables and visitation.
    
    Parameters:
    - data: pandas DataFrame containing visitation data and specified climate variables.
    
    This function calculates the correlation matrix for the specified climate variables and visitation,
    and visualizes it using a heatmap.
    
    Note: Understanding the correlation between climate factors and visitation can help identify trends and inform park management strategies.
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
    
    
# 3. Visualize yearly changes in the number of visitors across all parks on a single graph (line graph):
def visualize_park_visitation_trends(data):
    """
    Visualizes yearly visitation trends across all parks using a line graph.
    
    Parameters:
    - data: pandas DataFrame containing 'Year', 'Park Name', and 'Visitation' columns.
    
    This function plots a line graph for each park showing the change in visitation over the years.
    
    Note: This visualization allows for the comparison of visitation trends across different parks, 
          highlighting patterns or anomalies in visitor numbers.
    """
    # Getting unique park names
    unique_parks = data['Park Name'].unique()
    plt.figure(figsize=(14, 8))

    # Plotting visitation trends for each park
    for park in unique_parks:
        park_data = data[data['Park Name'] == park]
        plt.plot(park_data['Year'], park_data['Visitation'], marker='o', linestyle='-', label=park)

    # Configuring plot aesthetics
    plt.title('Yearly Visitation Trends Across All Parks')
    plt.xlabel('Year')
    plt.ylabel('Visitation')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()


# 4. Visualize yearly changes in the number of visitors across all parks on a single graph (area chart):
def visualize_park_visitation_trends_area(data):
    """
    Visualizes yearly visitation trends across all parks using an area chart.
    
    Parameters:
    - data: pandas DataFrame containing 'Year', 'Park Name', and 'Visitation' columns.
    
    This function plots an area chart for each park showing the change in visitation over the years.
    The area under each park's line is filled with color, and parks are stacked upon each other.
    
    Note: The area chart provides a visual representation of the cumulative visitation across parks, 
        allowing for an understanding of overall trends and the relative contribution of each park to total visitation.
    """
    # Getting unique park names
    unique_parks = data['Park Name'].unique()
    plt.figure(figsize=(14, 8))

    # Plotting an area chart for visitation trends for each park
    for park in unique_parks:
        park_data = data[data['Park Name'] == park].sort_values('Year')
        plt.fill_between(park_data['Year'], park_data['Visitation'], label=park, alpha=0.5)

    # Configuring plot aesthetics for the area chart
    plt.title('Yearly Visitation Trends Across All Parks (Area Chart)')
    plt.xlabel('Year')
    plt.ylabel('Visitation')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()


# 5. Compute and visualize the overall correlation:
def compute_and_visualize_correlation(data):
    """
    Computes and visualizes the correlation matrix for spending, visitation, and climate variables.
    
    Parameters:
    - data: pandas DataFrame containing 'Spending', 'Visitation', and climate variables.
    
    This function first cleans the data by dropping NA values, computes the correlation matrix, and then visualizes it using a heatmap.
    
    Note: The correlation matrix provides insights into the relationships between different variables, 
        which can inform decision-making and strategy for park management.
    """
    # Selecting relevant data for correlation analysis
    data_relevant = data[['Spending', 'Visitation', 'temp_avg', 'precip_sum', 'visibility', 'uvindex']].copy()

    # Clean data by dropping NA values and calculate the correlation matrix
    data_cleaned = data_relevant.dropna()
    correlation_matrix_cleaned = data_cleaned.corr()

    # Visualizing the correlation matrix using a heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix_cleaned, annot=True, fmt=".2f", cmap='coolwarm', 
                xticklabels=correlation_matrix_cleaned.columns, yticklabels=correlation_matrix_cleaned.columns)
    plt.title('Correlation Matrix of Visitation, Spending, and Climate variables')
    plt.show()


# 6. Analyze the growth rate of each park:
def analyze_growth_rate(data):
    """
    Analyzes the growth rate of visitation for each park and identifies the park with the highest and lowest average growth rate.
    
    Parameters:
    - data: pandas DataFrame containing 'Year', 'Park Name', and 'Visitation'.
    
    Returns:
    - A tuple containing the name of the top growing park, its average growth rate, the name of the top declining park, and its average growth rate.
    
    Note: This analysis helps identify parks that are rapidly gaining or losing popularity, 
        which could be useful for resource allocation and marketing efforts. 
        The park with the fastest growth rate is Kobuk Valley, with an infinite average growth rate, 
        indicating significant changes in the number of visitors. 
        This could occur when there is a substantial increase from years with very few visitors. 
        The park with the greatest decline is Olympic, with an average growth rate of approximately -1.32%.
    """
    # Calculate the change (%) in visitation and the average growth rate for each park by year
    visitation_growth = data.pivot_table(index='Year', columns='Park Name', values='Visitation').pct_change().mul(100)
    average_growth_rate = visitation_growth.mean().sort_values(ascending=False)
    
    # Identifying the top growing and declining parks
    top_growing_park = average_growth_rate.idxmax()
    top_declining_park = average_growth_rate.idxmin()

    return (top_growing_park, average_growth_rate[top_growing_park], top_declining_park, average_growth_rate[top_declining_park])


# 7. Compare the COVID period (2020-2023) with the period before and after:
def compare_covid_period(data):
    """
    Compares visitation, spending, and climate variables before and during the COVID-19 period (2020-2023).
    
    Parameters:
    - data: pandas DataFrame containing 'Year', 'Spending', 'Visitation', and climate variables.
    
    Prints summary statistics for the COVID-19 period (2020-2023) and the period before it, and returns the summaries as pandas DataFrames.
    
    Note: Summary analysis from 2020 to 2023 reveals the following:
    - Visitation and Spending: In 2020, the average number of visitors was about 1,078,281, 
                            with an average expenditure of $7,734. In 2021, 
                            the average number of visitors increased to approximately 1,464,315, 
                            with spending at an average of $7,907. In 2022, the visitation averaged around 1,407,336, 
                            with an average spending of $8,050. Data for 2023 shows missing visitor numbers, with an average expenditure of $7,889.
    - Climate Features: Average temperature, precipitation, visibility, and UV index 
                        showed minor changes during this period, with no significant overall deviations. 
                        In 2022 and 2023, severerisk data began to appear.
    - Comparison with the Preceding Period (before 2019): 
        Average expenditure and visitor numbers show no significant difference compared to the period before 2020. 
        Climate variables also displayed similar average values to the preceding period.
    - Analysis Conclusion: The observed decrease in visitor numbers in 2020 is 
                        presumed to be due to the COVID-19 pandemic, 
                        although a recovery trend is noted in 2021 and 2022. 
                        Expenditure remained relatively stable or showed a slight 
                        increasing trend during the pandemic. Climate variable averages 
                        did not change significantly during this period.
    """
    # Filtering data for 2020-2023
    data_2020_2023 = data[data['Year'].between(2020, 2023)]
    summary_2020_2023 = data_2020_2023.groupby('Year').mean()

    # Data before 2020
    data_pre_2020 = data[data['Year'] < 2020]
    summary_pre_2020 = data_pre_2020.groupby('Year').mean().mean()  # Average of averages before 2020

    print("Summary for 2020-2023 period:\n", summary_2020_2023)
    print("\nSummary for period before 2020:\n", summary_pre_2020)

    return summary_2020_2023, summary_pre_2020