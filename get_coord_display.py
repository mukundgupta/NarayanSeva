import requests

def get_coordinates(address):
    url = f"https://nominatim.openstreetmap.org/search?q={address}&format=json"

    response = requests.get(url, headers = {'User-Agent' : 'NarayanSeva/1.0 (mukundgupta2121@gmail.com)'})
    print(response)
    if response.status_code == 200:

        data = response.json()
        
        if data:
            
            lat = data[0]['lat']
            lon = data[0]['lon']
            print(f"lat:{lat},lon:{lon}")
            return lat,lon
        else:
            return "manual intervention required!"
            

