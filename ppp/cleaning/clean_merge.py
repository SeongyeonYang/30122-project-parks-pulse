import pandas as pd
import pathlib


def prepare_dataframe(df, park_name_col="park_name", year_col="year"):
    """clean park names and standardize year columns"""
    df[park_name_col] = df[park_name_col].str.strip()  # Clean park names
    if year_col in df.columns:
        df[year_col] = df[year_col].astype(str)  # Standardize year columns
    return df


# Load and prepare the time series data
filepath = pathlib.Path(__file__).parent / "cleaning/data/"
time_series = pd.read_csv(f"{filepath}cleaned_time_series.csv")
time_series = prepare_dataframe(time_series, "Park Name", "Year")

# Datasets to process
datasets = [
    ("acres", f"{filepath}np-fires-annual-acres.csv"),
    ("count", f"{filepath}np-fires-annual-count.csv"),
    (
        "dmr",
        f"{filepath}np-dmr-annual.csv",
        ["2015", "2016", "2017", "2018", "2019", "2023"],
    ),
    ("light", f"{filepath}/np-light-pollution-annual.csv"),
]

# Process and merge each dataset
for name, path, *optional in datasets:
    df = pd.read_csv(path)
    df = prepare_dataframe(df)

    if name == "dmr":  # Reshape the dmr DataFrame
        df = pd.melt(
            df,
            id_vars=["park_name"],
            value_vars=optional[0],
            var_name="year",
            value_name="dmr",
        )
        pattern = r"(?:(?:National Park of ) \
        |(?:National [a-zA-Z]+ of )|(?:))(.*?)(?: National [a-zA-Z]+|$)"
        df["park_name"] = df["park_name"].str.extract(pattern)[0]
        df["park_name"] = df["park_name"].replace("Sequoia and Kings Canyon", 
                                                  "Sequoia")
    df["year"] = df["year"].astype(str)

    # Rename 'park_name' to 'Park Name' for consistency
    df.rename(columns={"park_name": "Park Name", "year": "Year"}, inplace=True)

    # Merge with the main time_series DataFrame
    time_series = time_series.merge(df, how="left", on=["Year", "Park Name"])

time_series.drop(columns=["Unnamed: 0"], inplace=True)
time_series.to_csv(f"{filepath}cleaned_time_series_all.csv")
