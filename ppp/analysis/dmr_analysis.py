import pandas as pd
import pathlib
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.formula.api import ols


def get_data():
    filename = pathlib.Path(__file__).parents[1] / "cleaned_data/cleaned_time_series_all.csv"
    cols_to_use = ["Year", "Park Name", "Spending", "Visitation", "dmr"]
    df = pd.read_csv(filename, usecols=cols_to_use)

    df_dmr = df[["Year", "Park Name", "dmr"]]
    df = df.drop(["dmr"], axis=1)

    sliced_df = df[df['Park Name'].isin(["Kings Canyon", "Sequoia"])]
    df_combined = sliced_df.groupby("Year")[["Spending","Visitation"]].sum().reset_index()
    df_combined["Park Name"] = "Sequoia"

    df.drop(df.loc[df['Park Name'].isin(["Sequoia", "Kings Canyon"])].index, inplace=True)

    df_final = pd.concat([df, df_combined])
    df_final = df_final.merge(df_dmr, on=["Year", "Park Name"])
    df_final.dropna(inplace=True)

    return df_final


def regression():
    df = get_data()
    df["log_visitation"] = np.log(df["Visitation"])
    df["log_dmr"] = np.log(df["dmr"])
    df["log_spending"] = np.log(df["Spending"])

    df.replace([np.inf, -np.inf], np.nan, inplace=True)

    reg_result = ols("log_dmr ~ log_visitation + log_spending", data=df).fit()

    return reg_result


def print_regression_result():
    result = regression()

    with open(pathlib.Path(__file__).parent / "visualizations/regression_summary.txt", 'w') as fh:
        fh.write(result.summary().as_text())


def visualize_regression():
    result = regression()
    figure = sm.graphics.plot_partregress_grid(result)
    figure.tight_layout(pad=1.0)
    figure.suptitle('Partial Regression Plot: DMR, Visitation, and Spending at NPs (2015-2019)', fontsize=12)

    figure.savefig(pathlib.Path(__file__).parent / "visualizations/regression_plot.png")
