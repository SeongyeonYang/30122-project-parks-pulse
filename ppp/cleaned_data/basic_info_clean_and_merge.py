from pathlib import Path
import pandas as pd

# Function to find a partial match in the park names
def match_park_names(cleaned_name, other_names):
    for other_name in other_names:
        if cleaned_name in other_name:
            return other_name
    return None

# Define the file paths using pathlib
cleaned_nps_path = Path('ppp/cleaned_data/cleaned_nps_info.csv')
dmr_2023_path = Path('/hazards/cleaned_data/dmr-2023.csv')
merged_file_path = Path('ppp/cleaned_data/cleaned_nps_info.csv')
orphaned_wells_path = Path('/hazards/cleaned_data/orphaned_wells.csv')

# Load the datasets
cleaned_nps_df = pd.read_csv(cleaned_nps_path)
orphaned_wells_df = pd.read_csv(orphaned_wells_path)

# Match park names
cleaned_nps_df['matched_park_name'] = cleaned_nps_df['Park Name'].apply(
    lambda x: match_park_names(x, orphaned_wells_df['park_name']))

# Merge the dataframes
merged_df = pd.merge(cleaned_nps_df,
                     orphaned_wells_df,
                     left_on='matched_park_name',
                     right_on='park_name',
                     how='left')

# Drop unnecessary columns
columns_to_drop = ['Unnamed: 0', 'park_id', 'park_name', 'matched_park_name']
merged_df.drop(columns=columns_to_drop, inplace=True, errors='ignore')

# Fill NaN values
merged_df['abandoned_wells_count'] = merged_df['abandoned_wells_count'].fillna(merged_df['Abandoned_wells_count'])
merged_df.drop(columns=['Abandoned_wells_count'], inplace=True)
merged_df['state'] = merged_df['state'].fillna(merged_df['State'])
merged_df.drop(columns=['State'], inplace=True)

# Save the final merged dataframe to a CSV file
merged_df.to_csv(merged_file_path, index=False)


# Load the datasets
dmr_2023_df = pd.read_csv(dmr_2023_path)

# Create a new column for the partial matches
cleaned_nps_df['matched_park_name'] = cleaned_nps_df['Park Name'].apply(
    lambda x: match_park_names(x, dmr_2023_df['Park Name']))

# Perform the merge
merged_df = pd.merge(cleaned_nps_df,
                     dmr_2023_df,
                     left_on='matched_park_name',
                     right_on='Park Name',
                     how='left',
                     suffixes=('', '_dmr'))

# Drop the unmatched columns and the temporary matched_park_name column
merged_df.drop(columns=['matched_park_name', 'Park Name_dmr'], inplace=True, errors='ignore')

# Save the merged dataframe
merged_df.to_csv(merged_file_path, index=False)
