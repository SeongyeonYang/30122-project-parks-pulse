import pandas as pd
import pathlib
import re

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
    
def clean_daily_average(df):
    df['date_time'] = pd.to_datetime(df['DATE_TIME'], format='%m/%d/%Y %I:%M:%S %p', errors='coerce')
    df['date_only'] = df['date'].dt.strftime('%m-%d-%Y')
    df['month'] = pd.to_datetime(df['date_only']).dt.month
    
    df.set_index('date_only', inplace=True)