# Reference: https://gist.github.com/audhiaprilliant/9ad4e316c6d74a1c93a37836087fe3de#file-factor_analysis_composite_index-ipynb

import pandas as pd
import numpy as np
import pathlib
import matplotlib.pyplot as plt
import seaborn as sns
# Module for factor analysis
from factor_analyzer import FactorAnalyzer
# Module for adequacy test
from factor_analyzer.factor_analyzer import calculate_bartlett_sphericity
from factor_analyzer.factor_analyzer import calculate_kmo
# Module for standardization
from sklearn.preprocessing import MinMaxScaler
# Module for data viz
from plotnine import *
import plotnine

# Functions
def highlightLoadings(x):
    '''
    highlight the values if they are greater than 0.5 in a Series yellow.
    '''
    return ['background-color: yellow' if abs(v) > 0.5 else '' for v in x]

def highlightCommunalities(x):
    '''
    highlight the values if they are greater than 0.5 in a Series yellow.
    '''
    return ['background-color: yellow' if v > 0.5 else '' for v in x]

def highlightEigenvalue(x):
    '''
    highlight the values if they are greater than 1 in a Series yellow.
    '''
    return ['background-color: yellow' if v > 1 else '' for v in x]

# Path Setting
csv_filepath = pathlib.Path(__file__).parent.parent / "cleaning/cleaned_data/"
vis_filepath = pathlib.Path(__file__).parent.parent / "analysis/visualizations/"
# Data Preproccessing
nps_info_df = pd.read_csv(f'{csv_filepath}/cleaned_nps_info.csv')
time_series_df = pd.read_csv(f'{csv_filepath}/cleaned_time_series_all.csv')
park_code_df = pd.read_csv(f'{csv_filepath}/nps-parkcode.csv',
                           usecols=['SHORT','REGION'],  encoding='ISO-8859-1')
park_code_df.rename(columns={"SHORT": "Park Name"}, inplace=True)
park_code_df['Park Name'] = park_code_df['Park Name'].replace("National Park of American Samoa", "American Samoa")
park_code_df['Park Name'] = park_code_df['Park Name'].replace("Hawai'i Volcanoes", "Hawaii Volcanoes")
park_code_df['Park Name'] = park_code_df['Park Name'].replace("Wrangell-St. Elias", "Wrangell St Elias")
# Divided the baseline year temp
avg_temp_2011 = time_series_df[time_series_df['Year'] == 2011]. \
    groupby('Park Name')['temp_avg'].mean().reset_index()
avg_temp_2011.columns = ['Park Name', 'First_Year_Avg_Temp']
time_series_df = time_series_df.merge(avg_temp_2011, on='Park Name')
time_series_df['temp_avg'] = time_series_df['temp_avg'] \
                            / time_series_df['First_Year_Avg_Temp']
time_series_df.drop(columns=['First_Year_Avg_Temp'], inplace=True)

# Combine region
time_series_df = time_series_df.merge(park_code_df, on="Park Name", how='left')

# Fill NA with zero for fire data
time_series_df[['acres', 'count']] = time_series_df[['acres','count']].fillna(value=0)

# Using data from 2015 and merge it into info data
df_2015 = time_series_df[time_series_df["Year"] == 2015]
df_2019 = time_series_df[time_series_df["Year"] == 2019]
df_merge2015 = nps_info_df.merge(df_2015, on="Park Name", how='left')
df_merge2019 = nps_info_df.merge(df_2019, on="Park Name", how='left')

def data_prep(df):
    df.columns = df.columns.str.strip()
    df.drop(columns=["Year", "Unnamed: 0", 'precip_sum', "severerisk", 
            "light_pollution_ratio", "DM&R",  'Unpaved Road Miles',
        'Water Systems', 'Paved Road Miles',
        'All Other Assets'] , inplace=True)
    # Get rid of string columns
    df_fix = df.drop(columns=["Park Name", "State", "Location", 'REGION'])
    for column in df_fix.columns:
        df_fix[column] = pd.to_numeric(df_fix[column], errors='coerce')
    
    # Facility
    df_fix['water_facility'] = df_fix['Waste Water Systems'] / \
            (df_fix['Buildings'] + df_fix['Housing Units'] + df_fix['Campgrounds'] + 1)
    # Visitation normalize by trail miles
    #df_fix['Trail Miles'] = df_fix['Trail Miles'].replace(0, 1)
    #df_fix['Trail Miles'] = df_fix['Trail Miles'].fillna(1)
    #df_fix['Visitation'] = df_fix['Visitation'] / df_fix['Trail Miles']
    # Spending normalize by park size
    #df_fix['Spending'] = df_fix['Spending'] / df_fix['Size(Acres)']
    df_fix = df_fix.drop(columns=['Trail Miles', 'Size(Acres)', 'Buildings',
            'Housing Units', 'Campgrounds', 'Waste Water Systems'])
    # Fill up missing data
    column_means = df_fix.mean()
    df_fix = df_fix.fillna(column_means)
    # Standardize
    scaler = MinMaxScaler()
    df_scaled = pd.DataFrame(data = scaler.fit_transform(df_fix),
                            columns = df_fix.columns)
    # List of variables that have negative impact on park health
    negative_impact_vars = ['Abandoned_wells_within_30_miles', 'Active_wells_in_parks', 'At_risk',
                        'temp_avg', 'visibility', 'uvindex', 'acres', 'count', 'dmr']

    # Invert the scaled values for negatively impacting variables
    for var in negative_impact_vars:
        df_scaled[var] = 1 - df_scaled[var]
    
    return df_scaled

def adequacy_test(df_scaled, year):
    ## Adequacy test
    # Correlation
    df_corr = df_scaled.corr()
    plt.figure(figsize=(15, 10))
    sns.heatmap(df_corr, annot=True, cmap='coolwarm', center=0)
    plt.title('Correlation among all variables')
    plt.savefig(f'{vis_filepath}/{year}_Factor: Correlation among all variables.png')

    # Bartlett’s test
    chiSquareValue, pValue = calculate_bartlett_sphericity(df_scaled)
    print('Chi-square value : {}'.format(round(chiSquareValue, ndigits = 3)))
    print('p-value          : {}'.format(round(pValue, ndigits = 3)))

    # Kaiser-Meyer-Olkin test
    KMO, KMO_model = calculate_kmo(df_scaled)
    print('KMO value : {}'.format(round(KMO_model, ndigits = 3)))

    # Create factor analysis object and perform factor analysis
    fa = FactorAnalyzer(n_factors = 25, rotation = None)
    fa.fit(df_scaled)
    # The communalities
    df_communalities = pd.DataFrame(data = {'Column': df_scaled.columns, 'Communality': fa.get_communalities()})
    df_communalities.style.apply(highlightCommunalities, subset = ['Communality'])

    # Data viz
    plotnine.options.figure_size = (12, 9)
    communality_bar = (
        ggplot(data = df_communalities)+
        geom_bar(aes(x = 'Column',
                    y = 'Communality'),
                width = 0.75,
                stat = 'identity')+
        geom_hline(yintercept = 0.5)+
        scale_x_discrete(limits = df_communalities['Column'].tolist())+
        labs(title = 'Communalitites of factor analysis')+
        xlab('Columns')+
        ylab('Communalities')+
        theme_light()
    )
    # Save the graph
    communality_bar.save(filename = f'{vis_filepath}/{year}_communality_bar.png',
                        dpi = 1000,
                        verbose = False)

    # Check Eigenvalues
    eigenValue, value = fa.get_eigenvalues()
    eigenValue
    # Convert the results into a dataframe
    df_eigen = pd.DataFrame({'Factor': range(1, len(eigenValue) + 1), 'Eigen value': eigenValue})
    df_eigen.style.apply(highlightEigenvalue, subset = ['Eigen value'])

    plotnine.options.figure_size = (8, 4.8)
    scree_eigenvalue = (
        ggplot(data = df_eigen)+
        geom_hline(yintercept = 1)+
        geom_line(aes(x = 'Factor',
                    y = 'Eigen value'))+
        geom_point(aes(x = 'Factor',
                    y = 'Eigen value'),
                size = 2)+
        labs(title = 'Scree plot of eigen value from factor analysis')+
        xlab('Factors')+
        ylab('Eigenvalue')+
        theme_light()
    )
    # Save the graph
    scree_eigenvalue.save(filename = f'{vis_filepath}/{year}_scree_eigenvalue.png',
                        dpi = 1000,
                        verbose = False)
    return df_eigen

def factor_analysis(df, df_scaled, df_eigen, year):
    # Perform factor analysis
    # Number of factors
    n_factor = len(df_eigen[df_eigen['Eigen value'] > 1])
    print('Number of factors: {}'.format(n_factor))

    fa = FactorAnalyzer(n_factors = n_factor, rotation = None)
    fa.fit(df_scaled)

    # Create a factor's names
    facs = ['Factors' + ' ' + str(i + 1) for i in range(n_factor)]
    print(facs)

    # Loading factors
    # pd.DataFrame(data = fa.loadings_, index = df_scaled.columns, columns = facs).style.apply(highlightLoadings)
    # Explained variance
    idx = ['SS Loadings', 'Proportion Variance', 'Cumulative Variance']
    df_variance = pd.DataFrame(data = fa.get_factor_variance(), index = idx, columns = facs)
    df_variance.head()
    fa.get_factor_variance()
    # Ratio of variance
    ratioVariance = fa.get_factor_variance()[1] / fa.get_factor_variance()[1].sum()
    df_ratio_var = pd.DataFrame(data = ratioVariance.reshape((1, n_factor)), index = ['Ratio Variance'], columns = facs)
    df_ratio_var.head()
    # New completed dataframe
    df_ratio_variance = pd.concat([df_variance, df_ratio_var])
    df_ratio_variance.to_csv(f'{csv_filepath}/{year}_factor_ratio.csv')

    # The factor scores
    df_factors = pd.DataFrame(data = fa.fit_transform(df_scaled),
                            index = pd.MultiIndex.from_frame(df[['Park Name', 'REGION']]),
                            columns = facs)
    df_factors.head()

    scaler = MinMaxScaler()
    df_factors_scaled = pd.DataFrame(data = scaler.fit_transform(df_factors),
                                    index = pd.MultiIndex.from_frame(df[['Park Name', 'REGION']]),
                                    columns = facs)

    # Perform aggregation
    dict_index = {}
    for i in range(n_factor):
        key = df_factors_scaled.columns[i]
        value = df_factors_scaled.iloc[:,i].values * df_ratio_var.iloc[:,i].values
        dict_index.update({key:value})

    # Create a dataframe
    df_index = pd.DataFrame(dict_index,
                            index = pd.MultiIndex.from_frame(df[['Park Name', 'REGION']]))
    df_index['Composite Index'] = df_index.sum(axis = 1).values
    df_index['Rank'] = df_index['Composite Index'].rank(ascending = False)
    df_index = df_index.sort_values(by = 'Rank').reset_index()

    # Above and below the average
    stat = ['Above' if i > df_index['Composite Index'].mean() else 'Below' for i in df_index['Composite Index']]
    df_index['Status'] = stat
    df_index.to_csv(f'{csv_filepath}/{year}_factor_table.csv')

    # Summary statistic
    df_index['Composite Index'].describe()

    plotnine.options.figure_size = (8, 4.8)
    composite_index_distribution = (
        ggplot(data = df_index)+
        geom_density(aes(x = 'Composite Index'),
                    color = 'white',
                    fill = '#c22d6d')+
        labs(title = 'National Health Park Index 2015')+
        xlab('Composite Index')+
        ylab('Density')+
        theme_light()
    )
    # Save the graph
    composite_index_distribution.save(filename =  f'{vis_filepath}/{year}_composite_index_distribution.png',
                                    dpi = 1000,
                                    verbose = False)

# 2015
year = 2015
scaled_2015 = data_prep(df_merge2015)
df_eigen = adequacy_test(scaled_2015, year)
factor_analysis(df_merge2015, scaled_2015, df_eigen, year)

# 2019
year = 2019
scaled_2019 = data_prep(df_merge2019)
df_eigen = adequacy_test(scaled_2019, year)
factor_analysis(df_merge2019, scaled_2019, df_eigen, year)

# Region average score
index_2015 = pd.read_csv(f'{csv_filepath}/2015_factor_table.csv', usecols=['Park Name', 'REGION', 'Composite Index']).drop_duplicates()

average_composite_index = index_2015.groupby('REGION')['Composite Index'].mean().reset_index()
plt.figure()
sns.barplot(x='REGION', y='Composite Index', 
                data=average_composite_index, palette='viridis')
plt.xlabel('Region')
plt.ylabel('Average Composite Index')
plt.title('Average Composite Index among Regions')
plt.xticks(rotation=45)  # Rotate the region names for better readability
plt.subplots_adjust(bottom=0.2)
plt.savefig(f'{vis_filepath}/2015_Average Composite Index among Regions.png')