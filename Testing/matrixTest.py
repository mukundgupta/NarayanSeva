import requests

# store all coordinates in a string of the form longitude1,latitude1;lon2,lat2 ......

""" 
Point 1 -> my house
Point 2 -> BCM
Point 3 -> School
Point 4 -> NMIMS
"""
coord = "75.90626359940522,22.72748258309627;75.90081762245143,22.754022893354374;75.90080800995301,22.757286154164834;75.79402618302932,22.74969953952295"

# use OSRM HTML API by putting coordiantes in the url; annotations=distance makes the response contain distance instead of duration between coordinates
url =  f"http://router.project-osrm.org/table/v1/driving/{coord}?annotations=distance"

# get response using requests and convert it to json
response = requests.get(url).json()
print(response['distances'])