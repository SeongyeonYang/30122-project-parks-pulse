import pandas as pd
import pathlib
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from statsmodels.formula.api import ols


def get_data():
    """
    This function processes final cleaned time series data file for analysis.

    Inputs: None

    Returns: (DataFrame)
        Analysis-ready dataframe.
    """
    filename = pathlib.Path(__file__).parents[1] / "cleaning/cleaned_data/cleaned_time_series_all.csv"
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


def dmr_top_five():
    """
    This function returns the visualization for top five parks with the
    highest DMR in 2023.
    """
    filename = pathlib.Path(__file__).parents[1] / "cleaning/raw_data/dmr-2023.csv"
    df = pd.read_csv(filename, usecols=["Park Name", "totalDeferredMaintenance2023"])

    top_five = df.sort_values(['totalDeferredMaintenance2023'], ascending=False)[:5]
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=top_five, x="totalDeferredMaintenance2023",
                y="Park Name", hue="Park Name", ax=ax)
    ax.set_title("Top 5 NPs with highest Deferred Maintenance and Repair (2023)")
    ax.set_xlabel("Deferred Maintenance and Repair (USD)")
    plt.tight_layout()
    plt.savefig(pathlib.Path(__file__).parent /
                "visualizations/dmr-top-five-2023.png")


def regression():
    """
    This function runs multivariate regression of DMR on visitation and
    spending, all in log terms.
    """
    df = get_data()
    df["log_visitation"] = np.log(df["Visitation"])
    df["log_dmr"] = np.log(df["dmr"])
    df["log_spending"] = np.log(df["Spending"])

    df.replace([np.inf, -np.inf], np.nan, inplace=True)

    reg_result = ols("log_dmr ~ log_visitation + log_spending", data=df).fit()

    return reg_result


def print_regression_result():
    """
    This function saves to text the regression result summary.
    """
    result = regression()

    with open(pathlib.Path(__file__).parent / "visualizations/regression_summary.txt", 'w') as fh:
        fh.write(result.summary().as_text())


def visualize_regression():
    """
    This function saves to png the Partial Regression Plot.
    """
    print_regression_result()
    result = regression()
    figure = sm.graphics.plot_partregress_grid(result)
    figure.tight_layout(pad=1.0)
    figure.suptitle('Partial Regression Plot: DMR, Visitation, and Spending at NPs (2015-2019)', fontsize=12)

    figure.savefig(pathlib.Path(__file__).parent / "visualizations/regression_plot.png")
