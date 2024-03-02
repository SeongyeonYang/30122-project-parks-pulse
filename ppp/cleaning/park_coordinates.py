import requests
import json
import pandas as pd
import pathlib

def get_coordinates():
    API_Key_NPS = "UHG2SlVq8pBbBgr5SuGho6k0NJ6L5SPzu8DIjMXd" # Insert API key
    endpoint = "https://developer.nps.gov/api/v1/parks?"
    parameters = {"api_key":API_Key_NPS, "limit":500}
    response = requests.get(endpoint, params=parameters)
    print("response status code: " + str(response.status_code))
    data_all = response.json() # Interpret bytes as JSON format and convert to a Python dict
    # print('limit: ' + data_all['limit'])
    # print('total: ' + data_all['total'])
    # print('start: ' + data_all['start'])

    parks_data = []

    # Iterate over each park in the data
    for park in data_all['data']:
        # Extract the required information
        fullName = park['fullName']
        latitude = park['latitude']
        longitude = park['longitude']
        
        # Filter only National Park
        if "National Park" in fullName:
            parks_data.append({'Name':fullName, 'latitude': latitude, 'longitude': longitude})
    parks_df = pd.DataFrame(parks_data)
    filename = pathlib.Path(__file__).parent / "cleaning/data/parks_coordinates.csv"
    parks_df.to_csv(filename, index=False)
    return parks_data

get_coordinates()