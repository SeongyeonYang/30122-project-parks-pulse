import pandas as pd
import pathlib
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.formula.api import ols

def dmr_spend_rate():
    filename = pathlib.Path(__file__).parents[1] / "cleaned_data/cleaned_time_series_all.csv"
    cols_to_use = ["Year", "Park Name", "Spending", "Visitation", "dmr"]
    df = pd.read_csv(filename, usecols=cols_to_use)

    df.dropna(inplace=True)
    df["dmr_growth_rate"] = df.groupby(["Park Name"])["dmr"].pct_change()
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    dmr_df = df.groupby(["Park Name"])["dmr_growth_rate"].mean().to_frame(name="dmr_avg_annual_growth").reset_index()

    df["spend_growth_rate"] = df.groupby(["Park Name"])["Spending"].pct_change()
    spend_df = df.groupby(["Park Name"])["spend_growth_rate"].mean().to_frame(name="spend_avg_annual_growth").reset_index()

    pct_change_df = pd.merge(dmr_df, spend_df, on='Park Name', how='left')

    return pct_change_df


def plot_dr_spend():
    df = dmr_spend_rate()
    
    # stacked bar chart showing pct parks seeing improvement in addressing dmr and those not, of spending increases amount in each (decreasing over 2015-2019)
    new_df = df["dmr_avg_annual_growth"] > 0
    new_df_melted = pd.melt(df, id_vars=['Park Name'], value_vars=['dmr_avg_annual_growth','spend_avg_annual_growth'])


def regression():
    filename = pathlib.Path(__file__).parents[1] / "cleaned_data/cleaned_time_series_all.csv"
    cols_to_use = ["Year", "Park Name", "Spending", "Visitation", "dmr"]
    df = pd.read_csv(filename, usecols=cols_to_use)
    df.dropna(inplace=True)

    df["log_visit"] = np.log(df["Visitation"])
    df["log_dmr"] = np.log(df["dmr"])
    df["log_spend"] = np.log(df["Spending"])

    df.replace([np.inf, -np.inf], np.nan, inplace=True)

    reg_result = ols("log_dmr ~ log_visit + log_spend", data=df).fit()

    return reg_result


def print_regression_result():
    result = regression()

    with open('summary.txt', 'w') as fh:
        fh.write(result.summary().as_text())


def visualize_regression():
    result = regression()
    figure = sm.graphics.plot_partregress_grid(result)
    figure.tight_layout(pad=1.0)

    plt.show()




