import geopy
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="my_app")
location = geolocator.reverse("34.924, -107.899")

print(location.raw)