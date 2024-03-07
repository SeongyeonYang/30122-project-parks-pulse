import pathlib
import geopandas
import shapely
import pandas as pd
from scraper_light import get_light_data

# states with no national parks
NO_NP_STATES = ["WI", "IA", "IL", "NE", "KS", "OK", "LA", "MS", "AL",
                "GA", "PA", "MD", "DE", "NJ", "CT", "NY", "MA", "RI",
                "VT", "NH"]


def clean_fire_data():
    """
    This function cleaned raw fire data file to convert datatypes
    and shortlist relevant columns for processing.

    Inputs: None

    Returns: (DataFrame)
        Cleaned pandas dataframe with variables of interest in
        analysis-ready format.
    """
    filename = pathlib.Path(__file__).parent / "raw_data/nifc-fire.csv"
    cols_to_use = ["OBJECTID", "X", "Y", "FireDiscoveryDateTime",
                   "FinalAcres", "POOState"]
    df = pd.read_csv(filename, usecols=cols_to_use)

    df.rename(columns={"OBJECTID": "fire_id"}, inplace=True)
    df.rename(columns={"FireDiscoveryDateTime": "discovery_date"}, inplace=True)
    df.rename(columns={"FinalAcres": "acres"}, inplace=True)
    df.rename(columns={"POOState": "state"}, inplace=True)

    df["discovery_date"] = pd.to_datetime(df["discovery_date"].str[:10])
    df["state"] = df["state"].str[3:]
    df = df[~df["state"].isin(NO_NP_STATES)]
    df = df.reset_index(drop=True)

    return df


def clean_orphaned_wells():
    """
    This function cleaned raw orphaned wells file to filter NPs-related
    records and shortlist relevant columns for processing.

    Inputs: None

    Returns: (.csv)
        Cleaned .csv file of orphaned wells recorded for national parks.
    """
    filename = pathlib.Path(__file__).parent / "raw_data/npca-orphaned-wells.csv"
    df = pd.read_csv(filename)

    df.rename(columns={"UNIT_CODE": "park_id"}, inplace=True)
    df.rename(columns={"UNIT_NAME": "park_name"}, inplace=True)
    df.rename(columns={"UNIT_TYPE": "unit_type"}, inplace=True)
    df.rename(columns={"STATE": "state"}, inplace=True)
    df.rename(columns={"Abandoned Wells within 30 miles":
                       "abandoned_wells_within_30_miles"}, inplace=True)

    df = df[df["unit_type"] == "National Park"]
    df = df.drop("unit_type", axis=1)

    df.to_csv(pathlib.Path(__file__).parent /
              "cleaned_data/orphaned-wells.csv", index=False)


def clean_boundary():
    """
    This function extracted relevant columns of park boundaries geojson file.

    Inputs: None

    Returns: (DataFrame)
        Dataframe with relevant entries for national parks boundary data.
    """
    filename = pathlib.Path(__file__).parent / "raw_data/nps-boundary.geojson"
    df = geopandas.read_file(filename)

    df = df[["UNIT_CODE", "PARKNAME", "STATE", "geometry"]].copy()
    df.rename(columns={'UNIT_CODE':'park_id'}, inplace=True)
    df.rename(columns={'PARKNAME':'park_name'}, inplace=True)
    df.rename(columns={'STATE':'state'}, inplace=True)
    df.rename(columns={'geometry':'bbox'}, inplace=True)        

    return df


def clean_light_data():
    """
    This function cleans light data scraped from NPS webpage

    Inputs: None

    Returns: (.csv)
        Cleaned .csv file of light pollution data recorded for national parks.
    """
    df = get_light_data()
    df = df.drop(index=0)
    df = df.reset_index(drop=True)

    df["date_observed"] = df["date_observed"].str.strip()
    df["light_pollution_ratio"] = df["light_pollution_ratio"].str.strip()
    df["lon"] = df["lon"].str.strip()
    df["lat"] = df["lat"].str.strip()

    df["year"] = pd.DatetimeIndex(df["date_observed"]).year
    df = df.drop("date_observed", axis=1)

    df = df[df["park_name"].str.contains("NP")]
    df["park_name"] = df["park_name"].str.replace("\s+\S+$", "", regex=True)

    df.to_csv(pathlib.Path(__file__).parent /
              "cleaned_data/nps-light-pollution.csv", index=False)


def process_light_pollution():
    """
    This function processes cleans light data and convert datatypes to
    specific analysis-suitable formats. 

    Inputs: None

    Returns: (.csv)
        Processed and analysis-ready annual light pollution data.
    """
    filename = pathlib.Path(__file__).parent / "cleaned_data/nps-light-pollution.csv"
    cols_to_use = ["park_name", "year", "light_pollution_ratio"]
    df = pd.read_csv(filename, usecols=cols_to_use)

    standardized_df = df.copy()
    standardized_df.replace("< 0.04", 0, inplace=True)
    standardized_df["light_pollution_ratio"] =\
        pd.to_numeric(standardized_df["light_pollution_ratio"])

    time_series = standardized_df.groupby(["park_name", "year"])["light_pollution_ratio"].mean()

    time_series.to_csv(pathlib.Path(__file__).parent /
                       "cleaned_data/np-light-pollution-annual.csv")


def process_dmr():
    """
    This function merges deferred maintenance and repair data from 2 sources. 

    Inputs: None

    Returns: (.csv)
        Merged and analysis-ready annual (2015-2019, 2023) DMR data.
    """
    filename1 = pathlib.Path(__file__).parent / "raw_data/dmr-2015-2019.csv"
    filename2 = pathlib.Path(__file__).parent / "raw_data/dmr-2023.csv"
    df1 = pd.read_csv(filename1)
    df2 = pd.read_csv(filename2)

    df_merged = pd.merge(df1, 
                         df2[["Park Name", "totalDeferredMaintenance2023"]],
                         left_on="parkName", right_on="Park Name", how="left")

    df_merged = df_merged.drop(["Park Name", "stateAbbrev", "stateName"], axis=1)

    df_merged.rename(columns={"parkName": "park_name",
                              "totalDeferredMaintenance2015": "2015",
                              "totalDeferredMaintenance2016": "2016",
                              "totalDeferredMaintenance2017": "2017",
                              "totalDeferredMaintenance2018": "2018",
                              "totalDeferredMaintenance2019": "2019",
                              "totalDeferredMaintenance2023": "2023"},
                              inplace=True)

    df_merged = df_merged[["park_name", "2015", "2016", "2017", "2018", "2019", "2023"]]

    df_merged.to_csv(pathlib.Path(__file__).parent /
                     "cleaned_data/np-dmr-annual.csv", index=False)
