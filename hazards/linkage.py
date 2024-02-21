import shapely
import pathlib
import pandas as pd
from clean import clean_fire_data, clean_boundary


def fire_mapping():
    boundary = clean_boundary()
    fire = clean_fire_data()
    fire["park_name"] = None
    fire["park_id"] = None
    
    for i, fire_row in fire.iterrows():
        point = shapely.geometry.Point(fire_row["X"], fire_row["Y"])
        for _, boundary_row in boundary.iterrows():
            if fire_row["state"] == boundary_row["state"]:
                if point.within(boundary_row["bbox"]):
                    fire["park_name"].values[i] = boundary_row["park_name"]
                    fire["park_id"].values[i] = boundary_row["park_id"]
                    break
                break

    fire.to_csv("np-fire.csv")

# need to process this (delete none obs, recategorize by park and fire counts)