import requests
import folium

def get_coordinates(address):
    url = f"https://nominatim.openstreetmap.org/search?q={address}&format=json"

    response = requests.get(url, headers = {'User-Agent' : 'FoodRedistributor/1.0 (mukundgupta2121@gmail.com)'})
    print(response)
    if response.status_code == 200:

        data = response.json()
        if data:
            
            lat = data[0]['lat']
            lon = data[0]['lon']
            print(f"lat:{lat},lon:{lon}")
            return lat,lon
        else:
            print("Manual Intervention Required!")

def pr_map(coord):
    location = folium.Map(location=coord, zoom_start=16)
    folium.Marker(coord,popup = 'Location').add_to(location)

    location.save('map.html')
    print('location saved to map.html')

c = get_coordinates("BCM Heights, indore, india")
pr_map(c)