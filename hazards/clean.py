import pathlib
import geopandas
import shapely
import pandas as pd


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
    df.rename(columns={"Abandoned Wells within 30 miles": "abandoned_wells_count"}, inplace=True)

    df = df[df["unit_type"] == "National Park"]
    df = df.drop("unit_type", axis=1)

    df.to_csv("orphaned_wells.csv")


def clean_boundary():
    filename = pathlib.Path(__file__).parent / "data/nps-boundary.geojson"
    df = geopandas.read_file(filename)

    df = df[["UNIT_CODE", "PARKNAME", "STATE", "geometry"]].copy()
    df.rename(columns ={'UNIT_CODE':'park_id'}, inplace=True)
    df.rename(columns ={'PARKNAME':'park_name'}, inplace=True)
    df.rename(columns ={'STATE':'state'}, inplace=True)
    df.rename(columns ={'geometry':'bbox'}, inplace=True)        

    return df





    
