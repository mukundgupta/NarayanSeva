import requests #send request to OSRM
from ortools.constraint_solver import pywrapcp, routing_enums_pb2
import folium #displaying map


def main():
    
    data = {}
    data['locations'] = [
        [22.72986625513625,75.80408280922893],
        [22.72748258309627,75.90626359940522],
        [22.754022893354374,75.90081762245143],
        [22.720283605809062, 75.85661547732913],
        [22.757286154164834,75.90080800995301],
        [22.74969953952295,75.79402618302932]
        ]
    coord = ';'.join([f"{lon},{lat}" for lat, lon in data['locations']])
    """  hardcoded points for now
    Point 0 -> Airport --start-end 
    Point 1 -> my house 
    Point 2 -> BCM
    Point 3 -> random point (center of indore)
    Point 4 -> School
    Point 5 -> NMIMS
    
    Acceptors : 1,2,3
    Donors : 4,5
    Starting point: 0
    """
    
    data['food_types'] = {
        0:'Cooked Food',
        1:'Packaged Food'
    }

    data['acceptors'] = {
        1:{'requirement':30, 'type':0},
        2:{'requirement':50, 'type':1},
        3:{'requirement':20, 'type':0} 
        }
    
    data['donors'] = {
        4:{'type':0,'supply':50},
        5:{'type':1,'supply':50}
        }

    data['distanceMatrix'] = createDistanceMatrix(coord)
    print("DISTANCE MATRIX: ")
    for row in data['distanceMatrix']:
        print(row)
    data['start_end_point'] = 0
    manager = pywrapcp.RoutingIndexManager(len(data['distanceMatrix']),1,data['start_end_point'])
    routing = pywrapcp.RoutingModel(manager)
    
    routing.solver().Add(
    routing.NextVar(routing.Start(0)) >= manager.NodeToIndex(4)  # Start from a donor (index >= 4)
)
    print("\nSOLUTION")
    solution = solveBestRoute(data, manager, routing)
    

    route = []
    route_nodes = print_solution(manager, routing, solution,data)
    for node in route_nodes:
        index = manager.IndexToNode(node)
        if index < len(data['locations']):
            lat,lon = data['locations'][index]
            route.append((lat,lon))
 
    direct = display_route_on_map(route)
    print(direct)

    allocate_food(manager, routing, solution, data)

    return route_nodes,direct
    
    


def createDistanceMatrix(coordinates):
    # use OSRM HTML API by putting coordiantes in the url; annotations=distance makes the response contain distance instead of duration between coordinates
    url = f"http://router.project-osrm.org/table/v1/driving/{coordinates}?annotations=distance"
    response = requests.get(url).json()

    return response['distances']

def allocate_food(manager, routing, solution, data):
    """
    Function to allocate food to acceptors along the route by tracking the remaining supply"""
    remaining_supply = {donor_index: data['donors'][donor_index]['supply'] for donor_index in data['donors']}

    total_food_delivered = 0

    unfulfilled_acc = {}
    #iterating over all routes
    for route_index in range(routing.vehicles()):
        index = routing.Start(route_index) # start of route
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)

            #checking if current node is an acceptor
            if node_index in data['acceptors']:
                acceptor_type = data['acceptors'][node_index]['type']
                acceptor_req = data['acceptors'][node_index]['requirement']

                # finding a donor that has that food type in supply
                for donor_index, donor_info in data['donors'].items(): # returns a tuple with index and info
                    if donor_info['type'] == acceptor_type and remaining_supply[donor_index] > 0:
                        #Calculate amount of food to be delivered
                        food_amount_allocated = min(acceptor_req, remaining_supply[donor_index])

                        #Update remaining supply
                        remaining_supply[donor_index] -= food_amount_allocated
                        acceptor_req -= food_amount_allocated
                        total_food_delivered += food_amount_allocated 

                        print(f"Allocated {food_amount_allocated} units of food to Acceptor {node_index} from Donor {donor_index}")

                        if acceptor_req <= 0:
                            break
                if acceptor_req > 0:
                    unfulfilled_acc[node_index] = acceptor_req

            index = solution.Value(routing.NextVar(index))

    print("Allocation Complete\n")
    # Print remaining supplies after deliveries
    print("Remaining Supplies after delivery: ")
    for donor_index, supplies in remaining_supply.items():
        if supplies:
            print(f"Donor {donor_index}: {supplies} units of type {data['donors'][donor_index]['type']} remaining")
        else:
            print(f"Donor {donor_index}: All food allocated")
    
    if unfulfilled_acc:
        print("\nAcceptors whose needs could not be met: ")
        for i in unfulfilled_acc:
            print(f"Acceptor {i} has {unfulfilled_acc[i]} units of unmet needs. Food type: {data['acceptors'][i]['type']}")
    else:
        print("All acceptors needs were fulfilled")


def add_food_type_constraint(routing, data, manager):
    # Create CumulVar to track food type along the route
    food_type_dimension = routing.GetDimensionOrDie('food_type')
    
    # Iterate over donors to initialize the food type
    for donor_index in data['donors']:
        donor_type = data['donors'][donor_index]['type']
        
        # Set the vehicle's food type to the donor's type at the start
        routing.AddToAssignment(food_type_dimension.CumulVar(manager.NodeToIndex(donor_index)))

    # Add constraints to ensure food type compatibility between donors and acceptors
    for acceptor_index in data['acceptors']:
        acceptor_type = data['acceptors'][acceptor_index]['type']

        # Ensure that the vehicle's current food type matches the acceptor's required food type
        routing.solver().Add(
            food_type_dimension.CumulVar(manager.NodeToIndex(acceptor_index)) == acceptor_type
        )

def solveBestRoute(data, manager, routing):
    
    def distance_callback(to, fro):
        from_node = manager.IndexToNode(fro)
        to_node = manager.IndexToNode(to)
        return data['distanceMatrix'][from_node][to_node]
    callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(callback_index)

    #add_food_type_constraint(routing, data, manager)

    parameters = pywrapcp.DefaultRoutingSearchParameters()
    parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    solution = routing.SolveWithParameters(parameters)

    return solution
# printing solution (copied)
def print_solution(manager, routing, solution,data):
    """Prints the solution."""
    
    index = routing.Start(0)
    route_nodes = []
    plan_output = 'Route for volunteer:\n'
    route_distance = 0
    while not routing.IsEnd(index):
        route_nodes.append(index)
        plan_output += ' {} ->'.format(manager.IndexToNode(index))
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        if routing.IsEnd(index):
            route_distance += data['distanceMatrix'][previous_index][data['start_end_point']]
            route_nodes.append(index)
            break
        route_distance += data['distanceMatrix'][previous_index][index]
    plan_output += ' {}\n'.format(manager.IndexToNode(index))
    plan_output += 'Distance of the route: {} km \n'.format(route_distance/1000)
    print(plan_output)
    return route_nodes

def display_route_on_map(route):
    center = route[0]
    route_map = folium.Map(location = center, zoom_start = 13)
    
    for i,(lat,lon) in enumerate(route[0:len(route)-1]):
        
        folium.Marker([lat,lon], popup = f"Location {i}").add_to(route_map)
    
    complete_directions = ""
    for i in range(len(route)-1):
        start = route[i]
        end = route[i+1]

        a,directions = actual_path(start[0], start[1], end[0], end[1])    
     
        
        
        
    return directions

def actual_path(lat1, lon1, lat2, lon2):
    url = f"http://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}?overview=full&geometries=geojson&steps=true"
    response = requests.get(url).json()
    complete_route = response['routes'][0]['geometry']
    coords = complete_route['coordinates']
    converted_route = [(lat,lon) for lon, lat in coords]

    steps = response['routes'][0]['legs'][0]['steps']
    
    directions = []

    for step in steps:
        
        maneuver_type = step['maneuver']['type']
        modifier = step['maneuver'].get('modifier', '')
        exit_number = step['maneuver'].get('exit', '')
        distance = step['distance']

        if maneuver_type == 'turn' and modifier:
            instruction = f"Turn {modifier} after "
        elif maneuver_type == 'continue':
            instruction = "Continue Straight for "
        elif maneuver_type == 'Merge':
            instruction = 'Merge'
        elif maneuver_type == 'exit':
            exit_number = step['maneuver'].get('exit', '')
            instruction = f"Take exit {exit_number} after "
        elif maneuver_type == 'rotary':
            if exit_number:
                instruction = f"Take exit {exit_number} in the roundabout (rotary)"
            else:
                instruction = "Enter the roundabout and follow the road"
        elif maneuver_type == 'new name':
            instruction = "Follow road for "
        elif maneuver_type == 'arrive':
            instruction = "Arrived at location"
        else:
            instruction = maneuver_type
        

        directions.append(f" {instruction} {distance:.0f} meters")

    return converted_route, directions


main()