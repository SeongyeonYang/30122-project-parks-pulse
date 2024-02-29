import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Read files
nps_info_df = pd.read_csv('ppp/cleaned_data/cleaned_nps_info.csv')
time_series_df = pd.read_csv('ppp/cleaned_data/cleaned_time_series_all.csv')

def descriptive_stat(df, time_series_df):
    """
    Produce some descriptive statistics in our data.

    Args:
        df (dataframe): characteristics data
        time_series_df (dataframe): time series data
    """
    
    # Overall Visits Across All Parks for Available Years
    overall_visits_by_year = time_series_df.groupby('Year')['Visitation'].sum()
    
    # Total Number of National Parks
    total_parks = df['Park Name'].nunique()
    
    # Area of Each Park
    park_areas = df[['Park Name', 'Size(Acres)']]
    
    # Top 5 Visited Parks in 2022
    top_5_visited_2022 = time_series_df[time_series_df['Year'] == 2022] \
        .nlargest(5, 'Visitation')[['Park Name', 'Visitation']]
    
    # Compile statistics into a dictionary
    stats = {
        'overall_visits_by_year': overall_visits_by_year,
        'total_parks': total_parks,
        'park_areas': park_areas,
        'top_5_visited_2022': top_5_visited_2022
    }
    
    return stats

def descriptive_visualization(stats):
    """
    Visualize the stats from descriptive statistics

    Args:
        stats (dict): the stats we analysis
    """
    
    # Overall Visits by Year
    plt.figure(figsize=(10, 6))
    plt.plot(stats['overall_visits_by_year'].index, stats['overall_visits_by_year'].values, marker='o')
    plt.title('Overall National Park Visits by Year')
    plt.xlabel('Year')
    plt.ylabel('Total Visits')
    plt.grid(True)
    plt.show()
    
    # Park Areas
    plt.figure(figsize=(15, 10))  # Adjust the figure size as needed
    sns.barplot(x='Size(Acres)', y='Park Name', data=stats['park_areas'], palette='viridis')
    plt.title('National Parks by Size')
    plt.xlabel('Size(Acres)')
    plt.ylabel('Park Name')
    plt.show()
    
    # Top 5 Visited Parks in 2022
    plt.figure(figsize=(15, 5))
    sns.barplot(x='Visitation', y='Park Name', data=stats['top_5_visited_2022'], palette='viridis')
    plt.title('Top 5 Visited National Parks in 2022')
    plt.xlabel('Visitation')
    plt.ylabel('Park Name')
    plt.show()

# Climate visualization
def visualization_climate(time_series_df):
    """
    Visualization for climate data

    Args:
        time_series_df (dataframe)
    """
    # Preprocessing
    time_series_df = time_series_df[~time_series_df['Year'].isin([2023, 2024])]
    # Divided the baseline year temp
    avg_temp_2011 = time_series_df[time_series_df['Year'] == 2011]. \
        groupby('Park Name')['temp_avg'].mean().reset_index()
    avg_temp_2011.columns = ['Park Name', 'First_Year_Avg_Temp']
    time_series_df = time_series_df.merge(avg_temp_2011, on='Park Name')
    time_series_df['temp_avg'] = time_series_df['temp_avg'] \
                                / time_series_df['First_Year_Avg_Temp']
    time_series_df.drop(columns=['First_Year_Avg_Temp'], inplace=True)
    
    parks = time_series_df['Park Name'].unique()
    plt.figure(figsize=(15, 10))
    for park in parks:
        # Filter the DataFrame for each park
        park_df = time_series_df[time_series_df['Park Name'] == park]
        # Plot each park's average temperature over time
        sns.lineplot(x='Year', y='temp_avg', data=park_df, label=park)
        if not park_df.empty and park == "Denali":
            # Get the last year and temp_avg for the park
            last_year = park_df['Year'].values[-1]
            last_temp_avg = park_df['temp_avg'].values[-1]
            # Place text at the last point
            plt.text(last_year, last_temp_avg, park, fontsize=9, va='center')

    plt.title('Temperature Over Years for Each Park')
    plt.xlabel('Year')
    plt.ylabel('Average Temperature')
    plt.legend(title='Park Name', loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()  
    plt.show()
    
    # Plot for precipitation
    plt.figure(figsize=(15, 10))
    for park in parks:
        park_df = time_series_df[time_series_df['Park Name'] == park]
        sns.lineplot(x='Year', y='precip_sum', data=park_df, label=park)
        if not park_df.empty and park == "American Samoa":
            # Get the last year and temp_avg for the park
            last_year = park_df['Year'].values[-1]
            last_temp_avg = park_df['precip_sum'].values[-1]
            # Place text at the last point
            plt.text(last_year, last_temp_avg, park, fontsize=9, va='center')
    plt.title('Precipitation Sum Over Years for Each Park')
    plt.xlabel('Year')
    plt.ylabel('Precipitation Sum')
    plt.legend(title='Park Name', loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    plt.show()