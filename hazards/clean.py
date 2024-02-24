import pathlib
import geopandas
import shapely
import pandas as pd
from scraper import get_light_data


NO_NP_STATES = ["WI", "IA", "IL", "NE", "KS", "OK", "LA", "MS", "AL",
                "GA", "PA", "MD", "DE", "NJ", "CT", "NY", "MA", "RI",
                "VT", "NH"]


def clean_fire_data():
    filename = pathlib.Path(__file__).parent / "data/nifc-fire.csv"
    cols_to_use = ["OBJECTID", "X", "Y", "FireDiscoveryDateTime", "FinalAcres", "POOState"]
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
    filename = pathlib.Path(__file__).parent / "data/npca-orphaned-wells.csv"
    df = pd.read_csv(filename)

    df.rename(columns={"UNIT_CODE": "park_id"}, inplace=True)
    df.rename(columns={"UNIT_NAME": "park_name"}, inplace=True)
    df.rename(columns={"UNIT_TYPE": "unit_type"}, inplace=True)
    df.rename(columns={"STATE": "state"}, inplace=True)
    df.rename(columns={"Abandoned Wells within 30 miles": "abandoned_wells_within_30_miles"}, inplace=True)

    df = df[df["unit_type"] == "National Park"]
    df = df.drop("unit_type", axis=1)

    df.to_csv("orphaned-wells.csv")


def clean_boundary():
    filename = pathlib.Path(__file__).parent / "data/nps-boundary.geojson"
    df = geopandas.read_file(filename)

    df = df[["UNIT_CODE", "PARKNAME", "STATE", "geometry"]].copy()
    df.rename(columns={'UNIT_CODE':'park_id'}, inplace=True)
    df.rename(columns={'PARKNAME':'park_name'}, inplace=True)
    df.rename(columns={'STATE':'state'}, inplace=True)
    df.rename(columns={'geometry':'bbox'}, inplace=True)        

    return df


def clean_light_data():
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

    df.to_csv("np-light-pollution.csv")


def clean_pew_maintenance():
    filename = pathlib.Path(__file__).parent / "data/pew-maintenance.json"
    df = pd.read_json(filename)
    
    df.to_csv("pew-maintenance.csv")


def process_light_pollution():
    filename = pathlib.Path(__file__).parent / "cleaned_data/np-light-pollution.csv" # probably need to update path upon finalization
    cols_to_use = ["park_name", "year", "light_pollution_ratio"]
    df = pd.read_csv(filename, usecols=cols_to_use)

    standardized_df = df.copy()
    standardized_df.replace("< 0.04", 0, inplace=True)
    standardized_df["light_pollution_ratio"] = pd.to_numeric(standardized_df["light_pollution_ratio"])

    time_series_by_park = standardized_df.groupby(["park_name", "year"])["light_pollution_ratio"].mean()

    time_series_by_park.to_csv("np-light-pollution-annual.csv")
