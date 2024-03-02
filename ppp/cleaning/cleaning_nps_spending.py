import pandas as pd
from pathlib import Path

# Base directory for input and output files
input_base_dir = Path(__file__).parents[1] / "cleaning/raw_data/nps_spending"
output_base_dir = Path(__file__).parents[1] / "cleaning/cleaned_data/cleaned_nps_spending"

# Define the list of national parks for filtering
national_parks_list = [
    "Acadia", "American Samoa", "Arches", "Badlands",
    "Big Bend", "Biscayne", "Black Canyon of the Gunnison", "Bryce Canyon",
    "Canyonlands", "Capitol Reef", "Carlsbad Caverns", "Channel Islands",
    "Congaree", "Crater Lake", "Cuyahoga Valley", "Death Valley",
    "Denali", "Dry Tortugas", "Everglades", "Gates of the Arctic",
    "Gateway", "Glacier", "Glacier Bay", "Grand Canyon",
    "Grand Teton", "Great Basin", "Great Sand Dunes", "Great Smoky Mountains",
    "Guadalupe Mountains", "Haleakala", "Hawaii Volcanoes", "Hot Springs",
    "Indiana Dunes", "Isle Royale", "Joshua Tree", "Katmai",
    "Kenai Fjords", "Sequoia NP & Kings Canyon NP",
    "Kobuk Valley",
    "Lake Clark", "Lassen Volcanic", "Mammoth Cave", "Mesa Verde",
    "Mount Rainier", "New River Gorge", "North Cascades", "Olympic",
    "Petrified Forest", "Pinnacles", "Redwood", "Rocky Mountain",
    "Saguaro", "Shenandoah", "Theodore Roosevelt", "Virgin Islands",
    "Voyageurs", "White Sands", "Wind Cave", "Wrangell-Saint Elias",
    "Yellowstone", "Yosemite", "Zion"
]

def process_nps_spending_data(input_file_path, output_file_path, national_parks_list):
    """
    Processes a CSV file containing National Park Service spending data for 
    a specific year, filters based on a list of national parks, 
    selects specific columns, adds a year column,
    reorders the columns, and saves the processed data to a new CSV file.

    Args:
    - input_file_path (str): The file path of the input CSV file.
    - output_file_path (str): The file path where the processed 
                            CSV file will be saved.
    - national_parks_list (list): A list of national park names to filter the data.
    """
    # Loop through years from 2011 to 2024
    for year in range(2011, 2025):
        # Construct file paths
        input_file_path = input_base_dir / f'nps_spending_{year}.csv'
        output_file_path = output_base_dir / f'cleaned_nps_spending_{year}.csv'

        # Load the dataset
        data = pd.read_csv(input_file_path)
        
        # Filter the dataset for partial matches
        mask = data[data.columns[0]].apply(lambda x: any(park in str(x) for 
                                            park in national_parks_list))
        filtered_data = data[mask]
        
        # Selecting columns by index: Assuming 0 for the park names, 
        # and a specific column for Spending
        selected_columns_by_index = filtered_data.iloc[:, [0, 4]].copy()
        selected_columns_by_index.columns = ['National Park', 'Spending']
        
        # Adding the year column
        selected_columns_by_index['Year'] = str(year)
        
        # Reordering columns to place 'Year' first
        columns_reordered_by_index = ['Year', 'National Park', 'Spending']
        selected_columns_reordered = selected_columns_by_index[columns_reordered_by_index]
        
        # Save the adjusted dataframe to a new CSV file
        selected_columns_reordered.to_csv(output_file_path, index=False)
    

def merge_nps_spending_files(year_start, year_end, input_base_dir, output_file_path):
    """
    Merges CSV files containing National Park Service spending data for 
    a given range of years into a single file.
    
    Args:
    - year_start (int): The starting year for the range of files to merge.
    - year_end (int): The ending year for the range of files to merge (inclusive).
    - input_base_dir (str): The base directory where the input CSV files are located.
    - output_file_path (str): The file path where the merged CSV file will be saved.
    """
    # Generate file paths for the range of years
    file_paths = [input_base_dir / f'cleaned_nps_spending_{year}.csv' 
                  for year in range(year_start, year_end + 1)]
    
    # Load and concatenate all DataFrames
    dfs = [pd.read_csv(file_path) for file_path in file_paths]
    merged_df = pd.concat(dfs, ignore_index=True)
    
    # Save the merged DataFrame to the specified output file path
    merged_df.to_csv(output_file_path, index=False)
    
    print(f'Merged file saved to {output_file_path}')
    

def sort_and_clean_nps_data(input_file_path, output_file_path):
    """
    Loads a CSV file, removes commas from the 'Spending' column, 
    converts it to numeric, sorts the data first by 'National Park' and then 
    by 'Year', and saves the sorted data to a new CSV file.

    Args:
    - input_file_path (str): The file path of the input CSV file 
                            containing the NPS spending data.
    - output_file_path (str): The file path where the sorted and cleaned 
                            CSV file will be saved.
    """
    # Load the CSV file
    data = pd.read_csv(input_file_path)

    # Remove commas from the 'Spending' column and convert it to numeric
    data['Spending'] = data['Spending'].apply(lambda x: x.replace(',', '') 
                                              if isinstance(x, str) else x)
    data['Spending'] = pd.to_numeric(data['Spending'], errors='coerce')

    # Sort the DataFrame first by 'National Park' and then by 'Year'
    data_sorted = data.sort_values(by=['National Park', 'Year'])

    # Save the sorted DataFrame to the specified output file path
    data_sorted.to_csv(output_file_path, index=False)

    print(f'Sorted and cleaned file saved to {output_file_path}')
