import pandas as pd
import pathlib

df = pd.DataFrame()

def clean_climate(filename):
    data = pd.read_csv(filename)
    data['datetime'] = pd.to_datetime(data['datetime'], format='%Y-%m-%d', errors='coerce')
    data['Year'] = data['datetime'].dt.year
    # Define custom aggregation dictionary
    agg_dict = {
        'temp': 'mean',
        'precip': 'sum',
        'visibility': 'mean',
        'uvindex': 'mean',
        'severerisk': 'mean'
    }

    # Group by 'date' and 'park', then aggregate
    annual_data = data.groupby(['Year', 'name']).agg(agg_dict)
    annual_data.reset_index(inplace=True)
    # Adjust park names
    annual_data['name'] = annual_data['name'].str.extract('^(.*?) National Park')
    annual_data.rename(columns={
        'name': 'Park Name',
        'temp': 'temp_avg',
        'precip': 'precip_sum',
    }, inplace=True)
    return annual_data

raw_filepath = pathlib.Path(__file__).parent / "raw_data/climate/"
for i in range(1,10):
    cleaned_data = clean_climate(f"{raw_filepath}climate_{i}.csv")
    df = pd.concat([df, cleaned_data], ignore_index=True)
    
df.sort_values(by=['Year', 'Park Name'])
df['Park Name'].str.strip()

output_path = pathlib.Path(__file__).parent / "cleaning/data/"
output_filename = f"{output_path}cleaned_climate.csv"
df.to_csv(output_filename, index=False)
print(f"Annual data saved to {output_filename}")
