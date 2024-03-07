import pathlib
from fastkml import kml
import requests
import lxml.html
import pandas as pd


USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"


def get_parkname(string):
    """
    This function retrieves park name from a string.
    """
    delim = "\n"
    return string.split(delim)[0]


def get_link(string):
    """
    This function returns the link that is referenced in a string.
    """
    components = string.split()
    for char in components:
        if char.startswith("href"):
            link = char[6:-5]
    return link


def parse_kml():
    """
    This function parses the kml file and returns links associated with
    light pollution.

    Inputs: None

    Returns: (dict)
        A dictionary that with park's name and link for (key, val) pairs.
    """
    result = {}
    filename = pathlib.Path(__file__).parent / "raw_data/nps-nightsky-monitoring.kml"
    with open(filename) as myfile:
        doc = myfile.read()

    k = kml.KML()
    k.from_string(doc.encode("utf-8"))
    features = list(k.features())
    placemarks = list(features[0].features())

    for monitoring_loc in placemarks:
        if len(result) == max:
            break
        park_name = get_parkname(monitoring_loc.description)
        link = get_link(monitoring_loc.description)
        if park_name not in result:
            result[park_name] = []
        result[park_name].append(link)

    return result
        

def get_light_data():
    """
    This function scrapes light data from from weblinks.

    Inputs: None

    Returns: (.csv)
        A .csv file containing light data scraped.
    """
    result = []
    links = parse_kml()

    for park, observations in links.items():
        for observation in observations:
            response = requests.get(observation, headers={"User-Agent": USER_AGENT})
            root = lxml.html.fromstring(response.text)
            light_pollution_ratio = root.xpath("//table[3]//tr[5]/td[6]")[0].text_content()
            date_observed = root.xpath("//table[1]//tr[4]/td[2]")[0].text_content()
            lon = root.xpath("//table[2]//tr[4]/td[2]")[0].text_content()
            lat = root.xpath("//table[2]//tr[5]/td[2]")[0].text_content()
            result.append([park, date_observed, light_pollution_ratio, lon, lat])
    
    df = pd.DataFrame(result, columns =["park_name", "date_observed", "light_pollution_ratio", "lon", "lat"])

    return df
