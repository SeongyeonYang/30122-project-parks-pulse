import csv
import requests
import re
from bs4 import BeautifulSoup

def scrape_national_parks(url):
    response = requests.get(url)
    if response.status_code != 200:
        response.raise_for_status()
    
    # get the content from URL
    soup = BeautifulSoup(response.text, 'html.parser')

    # find the table and iterate through each row
    table = soup.find('table', {'class': "wikitable"})

    if table is None:
        raise ValueError('No valid table found')
    
    rows = table.find_all('tr')

    park_data = []

    for row in rows[1:]:
        # some parks name in header some not
        header = row.find('th')
        park_name = header.text.strip() if header else row.find('td').text.strip()
        cleaned_park_name = re.sub(r'[†*‡]', '', park_name).strip()

        cols = row.find_all('td')
        location = cols[1].find('a').text.strip() if header else cols[2].find('a').text.strip()
        
        visitors = int(cols[-2].text.strip().replace(',', ''))
        
        park_data.append([cleaned_park_name, location, visitors])
    
    return park_data


def save_to_file(data, filename = 'national_parks.csv'):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Park Name', 'Location', 'Visitors(2022)'])
        writer.writerows(data)


url = 'https://en.wikipedia.org/wiki/List_of_national_parks_of_the_United_States'
data = scrape_national_parks(url)
save_to_file(data)