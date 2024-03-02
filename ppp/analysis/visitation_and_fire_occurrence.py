import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

input_path = Path(__file__).parent.parent / 'cleaning' / 'cleaned_data' / 'cleaned_time_series_all.csv'
output_path1 = Path(__file__).parent.parent / 'cleaning' / 'cleaned_data' / 'parks_fire_occurrence.csv'
output_path2 = Path(__file__).parent/ 'visualizations' / 'Fire Occurrences vs. Next Year\'s Visitation.png'

# Load the complete data
data = pd.read_csv(input_path)

# Dropping unnecessary columns
data_cleaned = data.drop(['Unnamed: 0', 'Spending', 'temp_avg', 'precip_sum', \
                          'visibility', 'uvindex', 'severerisk', 'dmr', \
                            'light_pollution_ratio'], axis=1)

# Filling missing values in 'acres' and 'count' with 0, as no wildfire occurrence
data_cleaned[['acres', 'count']] = data_cleaned[['acres', 'count']].fillna(0)

# Dropping rows with missing 'Visitation' data
data_cleaned.dropna(subset=['Visitation'], inplace=True)

# Exporting the cleaned dataset to a new CSV file
data_cleaned.to_csv(output_path1, index=False)


# Aggregate the total fire occurrences by year across all parks
fire_occurrences_by_year = data_cleaned.groupby('Year')['count'].sum().reset_index()

# Plotting the total fire occurrences trend
plt.figure(figsize=(12, 6))
sns.lineplot(data=fire_occurrences_by_year, x='Year', y='count', marker='o')
plt.title('Total Fire Occurrences Trend Over the Years Across All Parks')
plt.xlabel('Year')
plt.ylabel('Total Fire Occurrences')
plt.grid(True)
plt.tight_layout()



# Filtering the dataset to include only rows with fire occurrences (count > 0)
fire_occurrences = data_cleaned[data_cleaned['count'] > 0].copy()

# shift the visitation data so that each fire occurrence year's visitation 
# is compared with the next year's visitation numbers.
fire_occurrences['Next Year Visitation'] = fire_occurrences.groupby('Park Name')['Visitation'].shift(-1)

# Dropping rows where Next Year Visitation is NaN, which happens for the last year of each park's data
fire_occurrences.dropna(subset=['Next Year Visitation'], inplace=True)

# Determine the subplot grid size based on the number of parks
num_parks = len(fire_occurrences['Park Name'].unique())
cols = 2
rows = np.ceil(num_parks / cols).astype(int)  # Ensure we have enough rows

# Plotting for the parks with fire occurrences
plt.figure(figsize=(14, rows * 5))

parks_with_occurrences = fire_occurrences['Park Name'].unique()

for i, park in enumerate(parks_with_occurrences, 1):
    plt.subplot(rows, cols, i)
    park_data = fire_occurrences[fire_occurrences['Park Name'] == park]
    
    # Plotting fire count on the primary axis
    ax1 = plt.gca()
    ax1.plot(park_data['Year'], park_data['count'], 'ro-', label='Fire Count')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Number of Fires', color='r')
    ax1.tick_params(axis='y', labelcolor='r')
    
    # Plotting next year's visitation on the secondary axis
    ax2 = ax1.twinx()
    ax2.plot(park_data['Year'], park_data['Next Year Visitation'], 'bx-', label='Next Year Visitation')
    ax2.set_ylabel('Next Year Visitation', color='b')
    ax2.tick_params(axis='y', labelcolor='b')
    
    plt.title(park)
    plt.xticks(rotation=45)

plt.tight_layout(pad=3.0)
plt.suptitle('Fire Occurrences vs. Next Year\'s Visitation', fontsize=16, y=1.05 + 0.05*rows)
plt.savefig(output_path2)