import pandas as pd

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

for i in range(1,9):
    filename = f"ppp/raw_data/climate/climate_{i}.csv"
    cleaned_data = clean_climate(filename)
    df = pd.concat([df, cleaned_data], ignore_index=True)
    
df.sort_values(by=['Year', 'Park Name'])
output_filename = f"ppp/data/climate/cleaned_climate.csv"
df.to_csv(output_filename, index=False)
print(f"Annual data saved to {output_filename}")