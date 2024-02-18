import requests
import csv
from bs4 import BeautifulSoup

def scrape_parks(url):
    response = requests.get(url)
    if response.status_code != 200:
        response.raise_for_status()
        
    soup = BeautifulSoup(response.text, 'html.parser')
    parks_table = soup.find('table', {'id': "id_parkList"})

    parks = []
    rows = parks_table.find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        if 'NP' in cells[0].text:
            park_name = cells[0].text.strip()
            location = cells[1].text.strip()
            parks.append([park_name,location])
    
    return parks


def save_to_file(data, filename = 'national_parks_location'):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Park Name', 'Location'])
        writer.writerows(data)


url = 'https://parkplanning.nps.gov/parks.cfm'
data = scrape_parks(url)
save_to_file(data, 'national_parks_location')