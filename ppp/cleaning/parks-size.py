import csv
import requests
from bs4 import BeautifulSoup
from pathlib import Path

def scrape_national_parks_size(url):
    """
    Scrape the size in acres of national parks from a given URL. 
    
    Parameters:
    - url (str): The URL of the webpage to scrape.

    Returns:
    - list of lists: A list of parks' name and parks' size for each national park.

    Raises:
    - HTTPError: If the response status code is not 200, indicating a failure in the request.
    """
    response = requests.get(url)
    if response.status_code != 200:
        response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('table')
    rows = table.find_all('tr')

    parks_size = []

    for row in rows[1:]:
        cols = row.find_all('td')
        park_name = cols[0].text.strip()
        park_size_acres = cols[1].text.strip().replace(',','')
        parks_size.append([park_name, park_size_acres])

    return parks_size

def save_to_file(data, filename):
    """
    Save the provided data to a CSV file.

    Parameters:
    - data (list of lists): The data to be saved.
    - filename (Path): The string representing the file path to save the CSV file.

    Returns:
    - None
    """
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Park Name', 'Size(Acres)'])
        writer.writerows(data)


url = 'https://www.terragalleria.com/parks/info/national-parks-by-area.html'
data = scrape_national_parks_size(url)
output_file = Path(__file__).parent / 'cleaned_data' / 'national_parks_size.csv'
save_to_file(data, filename = output_file)