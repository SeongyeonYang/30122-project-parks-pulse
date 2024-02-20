import pandas as pd
import pathlib
import re
import numpy as np

def clean_to_year(year):
    '''
    Clean raw data into annual data
    
    output: csv file
    '''
    months = ["01", "04", "07", "10"]
    filepath = pathlib.Path(__file__).parent / f"ppp/raw_data/climate/export_{year}"
    annual_data = pd.DataFrame()
    for month in months:
        # Dynamically find the start of the actual data
        filename = f"{filepath}{month}.csv" 
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            start_line = 0
            for i, line in enumerate(lines):
                if 'Part II - Data' in line:
                    start_line = i
                    break
        df = pd.read_csv(filename, header=start_line-1)
        annual_data = pd.concat([annual_data, df], ignore_index=True)
    
    return annual_data

def get_park_code(df):
    park_code = set()
    col_names = df.columns[1:]
    pattern = re.compile(r'^[A-Z]{4}-[A-Z]{2}')
    for col in col_names:
        if pattern.match(col):
            code = pattern.match(col).group()
            park_code.add(code)
    return park_code

def get_measurement(df, measure):
    park_measure = []
    park_code = get_park_code(df)
    for park in park_code:
        park_measure.append(park + "_" + measure)
    return park_measure

def reshape_long(df):
    measurement = ["O3_PPB", "PM2_5B_UG_M3_LC", "TMP_DEGC", "RNF_MM_HR", "SOL_W_M2"]
    reshaped_data = []
    for measure in measurement:
        val = get_measurement(df, measure)
        df_melted = df.melt(id_vars=['DATE_TIME'],value_vars=val, var_name='park', value_name=measure)
        df_melted['park'] = df_melted['park'].str.extract(r'([A-Z]{4}-[A-Z]{2})')[0]
        reshaped_data.append(df_melted)
    df_concat = pd.concat(reshaped_data)
    return df_concat
    
def calculate_daily(df):
    # Replace -999.0 with NaN and parse 'DATE_TIME' to datetime
    df.replace(-999.0, np.nan, inplace=True)
    df['DATE_TIME'] = pd.to_datetime(df['DATE_TIME'], format='%m/%d/%Y %I:%M:%S %p', errors='coerce')

    # Extract date and month from 'DATE_TIME'
    df['date'] = df['DATE_TIME'].dt.date
    df['month'] = df['DATE_TIME'].dt.month
    df['year'] = df['DATE_TIME'].dt.year

    # Drop the original 'DATE_TIME' column
    df.drop(columns=['DATE_TIME'], inplace=True)

    # Define custom aggregation dictionary
    agg_dict = {
        'TMP_DEGC': ['max', 'min', 'mean'],
        'O3_PPB': 'mean',
        'PM2_5B_UG_M3_LC': ['max', 'mean'],
        'RNF_MM_HR': 'mean',
        'SOL_W_M2': 'mean'
    }

    # Group by 'date' and 'park', then aggregate
    df_daily = df.groupby(['date', 'year', 'month', 'park']).agg(agg_dict)

    # Flatten MultiIndex columns and rename
    df_daily.columns = ['_'.join(col).strip() for col in df_daily.columns.values]
    df_daily.reset_index(inplace=True)

    # Rename columns for clarity
    df_daily.rename(columns={
        'TMP_DEGC_max': 'tmp_MAX',
        'TMP_DEGC_min': 'tmp_min',
        'TMP_DEGC_mean': 'tmp_avg',
        'O3_PPB_mean': 'o3_mean',
        'PM2_5B_UG_M3_LC_max': 'pm2.5_MAX',
        'PM2_5B_UG_M3_LC_mean': 'pm2.5_mean',
        'RNF_MM_HR_mean': 'rnf_mean',
        'SOL_W_M2_mean': 'sol_mean'
    }, inplace=True)

    # Convert 'date' back to datetime if needed for further operations
    df_daily['date'] = pd.to_datetime(df_daily['date'])
    df_daily.drop(columns=['tmp_MAX', 'tmp_min'], inplace=True)
    return df_daily

def calculate_annual(df):

    # Define custom aggregation dictionary
    agg_dict = {
        'tmp_avg': ['mean'],
        'o3_mean': 'mean',
        'pm2.5_MAX': ['max'],
        'pm2.5_mean': ['mean'],
        'rnf_mean': 'mean',
        'sol_mean': 'mean'
    }

    # Group by 'date' and 'park', then aggregate
    df_annual = df.groupby(['year', 'park']).agg(agg_dict)

    # Flatten MultiIndex columns and rename
    df_annual.columns = ['_'.join(col).strip() for col in df_annual.columns.values]
    df_annual.reset_index(inplace=True)
    return df_annual

# TODO: get site names and merge into the dataframe
# Output file
for i in range(2010, 2024):
    df = clean_to_year(i)
    reshaped_df = reshape_long(df)
    df_daily = calculate_daily(reshaped_df)
    annual_data = calculate_annual(df_daily)
    filepath = pathlib.Path(__file__).parent / f"ppp/data/climate/"
    output_filename = f"{filepath}climate_{i}.csv"
    annual_data.to_csv(output_filename, index=False)
    print(f"Annual data for {i} saved to {output_filename}")