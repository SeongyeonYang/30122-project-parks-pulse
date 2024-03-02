import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Load the dataset
input_path = Path(__file__).parent.parent / 'cleaning' / 'cleaned_data' / 'parks_fire_occurrence.csv'
output_path = Path(__file__).parent/ 'visualizations' / 'Fire Size Trend.png'

data = pd.read_csv(input_path)

# Aggregate the total area affected by fires for each year
fire_size_by_year = data.groupby('Year')['acres'].sum().reset_index()

# Plotting the trend in fire sizes over the years
plt.figure(figsize=(10, 6))
sns.lineplot(data=fire_size_by_year, x='Year', y='acres', marker='o', color='red')
plt.title('Trend in Fire Size Over the Years')
plt.xlabel('Year')
plt.ylabel('Total Area Affected (Acres)')
plt.grid(True)
plt.tight_layout()

plt.savefig(output_path)
