import requests
from .park_coordinates import get_coordinates
from time import sleep

# Example list of parks with dummy coordinates (replace with actual data)
parks = get_coordinates()

# Make API requests for each park, getting site info
def get_site_data(park, start_date, end_date):
    # Base URL for the WQP API
    base_url = 'https://www.waterqualitydata.us/data/Station/search?'
    params = {
        'lat': park['latitude'],
        'long': park['longitude'],
        'within': 10,  # Radius in miles, adjust as needed
        'startDateLo': start_date,
        'startDateHi': end_date,
        'mimeType': 'csv'  # CSV format
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        filename = f"ppp/raw_data/water_quality/{park['Name']}_site.csv"
        with open(filename, 'w') as file:
            file.write(response.text)
        print(f"Data for {park['Name']} saved successfully.")
    else:
        print(f"Failed to retrieve data for {park['Name']}: {response.status_code}")

def get_water_quality(park, start_date, end_date, dataProfile):
    # Base URL for the WQP API
    base_url = 'https://www.waterqualitydata.us/data/Result/search?'
    params = {
        'lat': park['latitude'],
        'long': park['longitude'],
        'within': 5,  # Radius in miles, adjust as needed
        'startDateLo': start_date,
        'startDateHi': end_date,
        'sampleMedia': 'Water',
        'dataProfile': dataProfile,
        'mimeType': 'csv'  # CSV format
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        filename = f"ppp/raw_data/water_quality/{park['Name']}_quality_{dataProfile}.csv"
        with open(filename, 'w') as file:
            file.write(response.text)
        print(f"{dataProfile} Data for {park['Name']} saved successfully.")
    else:
        print(f"Failed to retrieve {dataProfile} data for {park['Name']}: {response.status_code}")

# Loop through each park and make the API request
for park in parks:
    get_site_data(park, "01-01-2010", "12-31-2023")
    get_water_quality(park, "01-01-2010", "12-31-2023", 'resultPhysChem')
    get_water_quality(park, "01-01-2010", "12-31-2023", 'biological')
    sleep(1)  # Pause between requests to avoid rate limiting
