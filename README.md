# NarayanSeva - A web application to reduce World Hunger


FUNCTIONS AND MODULE DESCRIPTIONS

link to GitHub repository -> https://github.com/mukundgupta/NarayanSeva

This is a platform designed to further the UN SDG-2 Zero Hunger. Our application connects donors i.e. places where food is in excess and may be wasted (schools, grocery stores, restaurants, bakeries and the like ) to places that require food to be donated (food banks, orphanages, free food centers for the homeless etc.).

We were inspired by various initiatives our school takes for service to the underprivileged. 
It is a deeply rooted belief of our school that divinity resides in every one of us, hence, we refer to the underprivileged as Narayans. The service to the Narayans is NarayanSeva.

For grocery stores, supermarkets and bakeries, the application offers an option to track the units of food remaining and notifies the store if an item is nearing expiry, asking if they wish to donate the items which are unlikely to sell in the last few days. If they agree, our app will add the location to the list of places where food will be collected from.

The application allows schools and restaurants to input the amount of food that is left for the day, and our application figures out the number of people it will be able to feed and inputs them into an algorithm.

The algorithm determines the best route that a volunteer should follow to collect and deliver food, as well as allocating required amounts of food based on the type of food and vicinity.



Following are general descriptions of various modules used along with documentation of functions we made.
Each module contains comments explaining how it works in code.



# Instructions to run locally

After downloading the folder, ensure that all modules are installed (create a virtual environment if necessary)
To use virtual environment, ensure that "virtualenv" is installed, then run 
(for windows)
```
python -m venv venv
venv\Scripts\activate
```
To install necessary modules, please run:```
``` 
pip install -r requirements.txt
```
If this does not work, please manually install the modules listed under "Requirements".

After installation:
From a terminal with the path of the folder, run ```

```
python app.py
```

This will launch the web application running locally (http://127.0.0.1:5000)
# Requirements

- Flask -to integrate with HTML
- OR-TOOLS - to create the best route 
- OSRM - to create a distance matrix and get directions of the created route
- OpenStreepMap Nominatim - getting coordinates from address input by users
- Requests - send HTTP requests to OSRM, OSM
- Folium - To display the map with the created route
- csv - storing provided data in a csv file

# Other platforms used
- codepen.io -> for some UI elements (HTML/CSS/JS)
- Several other UI elements were taken from a website we made for a different event, called SnapService, the repository for which is https://github.com/mukundgupta/snapservice-final
# Module Descriptions

Program runs from app.py using flask. It imports several other modules we made. 

### addDonorData.py

	Takes a list with donor data as argument. Generates an ID, attempts to get   coordinates(latitude, longitude) from the provided address using get_coord_display.py and then appends data to a CSV file (donorData.csv)

Functions in module:
- get_id()
-  add_donor_data(donor_data)


## get_coords_display.py

	Uses requests modules to send request to OpenStreetMap Nominatim API for the coordinates of the provided address. 
	If coordinates are found, returns the coordinates, else returns "manual intervention required!" to allow us to manually input coordinates for that address.
Functions in module:
- get_coordinates()


### addAcceptorData.py

	Takes a list with acceptor data as argument. Generates an ID, attempts to get   coordinates(latitude, longitude) from the provided address using get_coord_display.py and then appends data to a CSV file (acceptorData.csv)

Functions in module:
- get_id()
-  add_donor_data(donor_data)


## check_expiry.py
```
	Uses a dictionory of stores which contains units of items remaining along with their expiry, and if an item is close to expiry, adds the store to a list of stores to be notified.
Currently does not notify stores as that requires integration with an SMS or EMAIL API
Not imported in main function as of now
```

## main.py

	Program used to optimise the route using ortools, embed the route in a map.html file using folium and output the route along with directions to app.py
	
Functions in module:
- createDistanceMatrix(coordinates):
	- Uses OSRM (Open Source Routing Machine) HTML API to get a distance matrix of all locations (a matrix where element (ij) = distance from i to j)
	- Returns the distance matrix as a list


- solveBestRoute(data, manager, routing):
	- Uses a function get_distance() and registers it with the routing model from or-tools
	- Solves for the best route using PATH_CHEAPEST_ARC from or-tools
	- Returns the solution


- print_solution(manager, routing, solution, data):
	- Prints the route in the terminal
	- Returns the nodes of the routes in order as a list


- actual_path(lat1,lon1,lat2,lon2):
	- Uses OSRM to get the exact path of the route, with all the coordinates for turns
	- Gets turn -by-turn directions of each path
	- Returns the route and the directions of the segment in a list


- display_route_on_map(route):
	- marks location in a map.html file along with lines for path followed, using folium
	- computes the full route from segments from actual_path() function
	- returns the complete directions of the route as text


- allocate_food(manager, routing, solution, data):
	- allocates quantity of food from donors to acceptors, by keeping track of the total supply after visiting each location
	- stores the allocation in a list so that it can be displayed in HTML
	- Notifies if food is still left after delivery, or if any acceptor's needs could not be completely fulfilled
	- returns a list of all allocations which can be put displayed in an HTML page


- main():
	- uses all the above functions to output the data to be displayed in HTML
	- gets details of new donors, if any, and adds their location to algorithm if valid.



Flask also connects with HTML to get the form data using request.get()
Basic JavaScript used for UI elements as well as displaying csv data.

