import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pathlib

# Read files
csv_filepath = pathlib.Path(__file__).parent.parent / "cleaning/cleaned_data/"
vis_filepath = pathlib.Path(__file__).parent.parent / "analysis/visualizations/"
nps_info_df = pd.read_csv(f'{csv_filepath}/cleaned_nps_info.csv')
time_series_df = pd.read_csv(f'{csv_filepath}/cleaned_time_series_all.csv')
park_code_df = pd.read_csv(f'{csv_filepath}/nps-parkcode.csv',
                           usecols=['SHORT','REGION'],  encoding='ISO-8859-1')
park_code_df.rename(columns={"SHORT": "Park Name"}, inplace=True)
park_code_df['Park Name'] = park_code_df['Park Name'].replace("National Park of American Samoa", "American Samoa")
park_code_df['Park Name'] = park_code_df['Park Name'].replace("Hawai'i Volcanoes", "Hawaii Volcanoes")
park_code_df['Park Name'] = park_code_df['Park Name'].replace("Wrangell-St. Elias", "Wrangell St Elias")

# Preprocessing
# Drop 2023,2024
time_series_df = time_series_df[~time_series_df['Year'].isin([2023, 2024])]
# Divided the baseline year temp
avg_temp_2011 = time_series_df[time_series_df['Year'] == 2011]. \
    groupby('Park Name')['temp_avg'].mean().reset_index()
avg_temp_2011.columns = ['Park Name', 'First_Year_Avg_Temp']
time_series_df = time_series_df.merge(avg_temp_2011, on='Park Name')
time_series_df['temp_avg'] = time_series_df['temp_avg'] \
                            / time_series_df['First_Year_Avg_Temp']
time_series_df.drop(columns=['First_Year_Avg_Temp'], inplace=True)
# Combine region
time_series_df = time_series_df.merge(park_code_df, on="Park Name", how='left')


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
    
    # Overall Visits by Year(We already have)
    # plt.figure(figsize=(10, 6))
    # plt.plot(stats['overall_visits_by_year'].index, 
             # stats['overall_visits_by_year'].values, marker='o')
    # plt.title('Overall National Park Visits by Year')
    # plt.xlabel('Year')
    # plt.ylabel('Total Visits')
    # plt.grid(True)
    # plt.savefig(f'{vis_filepath}Overall National Park Visits by Year.png')
    
    # Park Areas
    plt.figure(figsize=(15, 10))  # Adjust the figure size as needed
    sns.barplot(x='Size(Acres)', y='Park Name', 
                data=stats['park_areas'], palette='viridis')
    plt.title('National Parks by Size')
    plt.xlabel('Size(Acres)')
    plt.ylabel('Park Name')
    plt.savefig(f'{vis_filepath}/National Parks by Size.png')
    
    # Top 5 Visited Parks in 2022
    plt.figure(figsize=(15, 5))
    sns.barplot(x='Visitation', y='Park Name', 
                data=stats['top_5_visited_2022'], palette='viridis')
    plt.title('Top 5 Visited National Parks in 2022')
    plt.xlabel('Visitation')
    plt.ylabel('Park Name')
    plt.savefig(f'{vis_filepath}/Top 5 Visited National Parks in 2022.png')

# Climate visualization
def visualization_climate(time_series_df):
    """
    Visualization for climate data

    Args:
        time_series_df (dataframe)
    """
    # Temperature for each park
    parks = time_series_df['Park Name'].unique()
    fig, ax = plt.subplots(figsize=(15, 3))
    for park in parks:
        park_df = time_series_df[time_series_df['Park Name'] == park].sort_values('Year')
        ax.plot(park_df['Year'], park_df['temp_avg'], label=park)
        if not park_df.empty and park == "Denali":
            # Get the last year and temp_avg for the park
            last_year = park_df['Year'].values[-1]
            last_temp_avg = park_df['temp_avg'].values[-1]
            # Place text at the last point
            ax.text(last_year, last_temp_avg, park, fontsize=9, va='center')
    ax.set_title('Average Temperature Over Years for Each Park')
    ax.set_xlabel('Year')
    ax.set_ylabel('Average Temperature')
    ax.legend(title='Park Name', loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig(f'{vis_filepath}/Average Temperature Over Years for Each Park.png')
    
    # Temperature for each region
    avg_temp_region = time_series_df.groupby(['REGION', 'Year'])['temp_avg'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=avg_temp_region, x='Year', y='temp_avg', hue='REGION', marker='o', ax=ax)
    ax.set_title('Average Temperature Over Years for Each Region')
    ax.set_xlabel('Year')
    ax.set_ylabel('Average Temperature')
    ax.legend(title='Region')
    plt.tight_layout()
    plt.savefig(f'{vis_filepath}/Average Temperature Over Years by Region.png')

    # Plot for precipitation
    fig, ax = plt.subplots(figsize=(15, 7))
    for park in parks:
        park_df = time_series_df[time_series_df['Park Name'] == park].sort_values('Year')
        ax.plot(park_df['Year'], park_df['precip_sum'], label=park)
        ax.fill_between(park_df['Year'], park_df['precip_sum'], alpha=0.3)
        if not park_df.empty and park == "American Samoa":
            # Get the last year and temp_avg for the park
            last_year = park_df['Year'].values[-1]
            last_temp_avg = park_df['precip_sum'].values[-1]
            # Place text at the last point
            ax.text(last_year, last_temp_avg, park, fontsize=9, va='center')
    ax.set_title('Precipitation Sum Over Years for Each Park')
    ax.set_xlabel('Year')
    ax.set_ylabel('Precipitation Sum')
    ax.legend(title='Park Name', loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    plt.savefig(f'{vis_filepath}/Precipitation Sum Over Years for Each Park.png')
    
    # Precipitation for each region
    sum_perp_region = time_series_df.groupby(['REGION', 'Year'])['precip_sum'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=sum_perp_region, x='Year', y='precip_sum', hue='REGION', marker='o', ax=ax)
    ax.set_title('Precipitation Sum Over Years for Each Region')
    ax.set_xlabel('Year')
    ax.set_ylabel('Precipitation Sum')
    ax.legend(title='Region')    
    plt.tight_layout()
    plt.savefig(f'{vis_filepath}/Precipitation Sum Over Years by Region.png')
    
stats = descriptive_stat(nps_info_df, time_series_df)
descriptive_visualization(stats)
visualization_climate(time_series_df)