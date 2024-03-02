from pathlib import Path
import pandas as pd

def match_park_names(cleaned_name, other_names):
    """
    Finds a partial match in the park names.

    Args:
        cleaned_name (str): The cleaned park name to match.
        other_names (pd.Series): A pandas Series containing park names 
                                to match against.

    Returns:
        str or None: The matched park name if found, otherwise None.
    """
    for other_name in other_names:
        if cleaned_name in other_name:
            return other_name
    return None

def merge_datasets(left_df, right_df, left_on, right_on, output_file):
    """
    Merges two DataFrames based on specified columns and 
    appends the result to a CSV file.

    Args:
        left_df (pd.DataFrame): The left DataFrame.
        right_df (pd.DataFrame): The right DataFrame.
        left_on (str): The column name in the left DataFrame to merge on.
        right_on (str): The column name in the right DataFrame to merge on.
        output_file (str): The path to save the merged DataFrame as a CSV file.
    """
    merged_df = pd.merge(left_df,
                         right_df,
                         left_on=left_on,
                         right_on=right_on,
                         how='left',
                         suffixes=('', '_right'))

    # Check if the output file exists
    file_exists = Path(output_file).exists()

    # Write the DataFrame to CSV
    merged_df.to_csv(output_file, mode='a', index=False, header=not file_exists)

cleaned_nps_path = Path(__file__).parents[1] / "cleaning/cleaned_data/cleaned_nps_info.csv"
orphaned_wells_path = Path(__file__).parents[1] / "cleaning/cleaned_data/orphaned_wells.csv"
dmr_2023_path = Path(__file__).parents[1] / "cleaning/data/hazards_cleaned/dmr-2023.csv"
output_file_path = Path(__file__).parents[1] / "cleaning/cleaned_data/cleaned_nps_info.csv"

# Load datasets
cleaned_nps_df = pd.read_csv(cleaned_nps_path)
orphaned_wells_df = pd.read_csv(orphaned_wells_path)
dmr_2023_df = pd.read_csv(dmr_2023_path)

# Merge cleaned_nps_df with orphaned_wells_df
cleaned_nps_df['matched_park_name'] = cleaned_nps_df['Park Name'].apply(lambda x: 
                        match_park_names(x, orphaned_wells_df['park_name']))
merge_datasets(cleaned_nps_df, orphaned_wells_df, 'matched_park_name', 
               'park_name', output_file_path)

# Merge 
cleaned_nps_df['matched_park_name'] = cleaned_nps_df['Park Name'].apply(lambda x: 
                                match_park_names(x, dmr_2023_df['Park Name']))
merge_datasets(cleaned_nps_df, dmr_2023_df, 'matched_park_name', 'Park Name', 
               output_file_path)
