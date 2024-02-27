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

    df.to_csv(pathlib.Path(__file__).parent / "cleaned_data/orphaned-wells.csv", index=False)


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

    df.to_csv(pathlib.Path(__file__).parent / "data/nps-light-pollution.csv", index=False)


def process_light_pollution():
    filename = pathlib.Path(__file__).parent / "data/nps-light-pollution.csv"
    cols_to_use = ["park_name", "year", "light_pollution_ratio"]
    df = pd.read_csv(filename, usecols=cols_to_use)

    standardized_df = df.copy()
    standardized_df.replace("< 0.04", 0, inplace=True)
    standardized_df["light_pollution_ratio"] = pd.to_numeric(standardized_df["light_pollution_ratio"])

    time_series_by_park = standardized_df.groupby(["park_name", "year"])["light_pollution_ratio"].mean()

    time_series_by_park.to_csv(pathlib.Path(__file__).parent / "cleaned_data/np-light-pollution-annual.csv", index=False)


def process_dmr():
    filename1 = pathlib.Path(__file__).parent / "data/dmr-2015-2019.csv"
    filename2 = pathlib.Path(__file__).parent / "data/dmr-2023.csv"
    df1 = pd.read_csv(filename1)
    df2 = pd.read_csv(filename2)
    result = []

    df_merged = pd.merge(df1, 
                         df2[["Park Name", "totalDeferredMaintenance2023"]],
                         left_on="parkName", right_on="Park Name", how="left")

    df_merged = df_merged.drop("Park Name", axis=1)

    for i, row in df_merged.iterrows(): # not necessary. clean up code later
        park_name = row["parkName"]
        dmr2015 = row["totalDeferredMaintenance2015"]
        dmr2016 = row["totalDeferredMaintenance2016"]
        dmr2017 = row["totalDeferredMaintenance2017"]
        dmr2018 = row["totalDeferredMaintenance2018"]
        dmr2019 = row["totalDeferredMaintenance2019"]
        dmr2023 = row["totalDeferredMaintenance2023"]
        result.append([park_name, dmr2015, dmr2016, dmr2017, dmr2018, dmr2019, dmr2023])

    dmr_time_series = pd.DataFrame(result, columns =["park_name", "2015", "2016", "2017", "2018", "2019", "2023"])

    dmr_time_series.to_csv(pathlib.Path(__file__).parent / "cleaned_data/np-dmr-annual.csv", index=False)
