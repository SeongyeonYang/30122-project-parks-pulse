import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
data = pd.read_csv('../../cleaned_data/parks_fire_occurrence.csv')

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

plt.savefig('../visualizations/Fire Size Trend.png')
