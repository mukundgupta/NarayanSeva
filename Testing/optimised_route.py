import requests
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

def main():

    data = {}

    coord = "75.90626359940522,22.72748258309627;75.90081762245143,22.754022893354374;75.90080800995301,22.757286154164834;75.79402618302932,22.74969953952295"
    """  hardcoded points for now
Point 0 -> my house
Point 1 -> BCM
Point 2 -> School
Point 3 -> NMIMS
"""
    data['distanceMatrix'] = createDistanceMatrix(coord)
    print("DISTANCE MATRIX: ")
    for row in data['distanceMatrix']:
        print(row)
    data['start_end_point'] = 2
    manager = pywrapcp.RoutingIndexManager(len(data['distanceMatrix']),1,[2],[3])
    routing = pywrapcp.RoutingModel(manager)
    
    print("\nSOLUTION")
    solution = solveBestRoute(data, manager, routing)
    print(solution)

    print_solution(manager, routing, solution,data)






def createDistanceMatrix(coordinates):
    # use OSRM HTML API by putting coordiantes in the url; annotations=distance makes the response contain distance instead of duration between coordinates
    url = f"http://router.project-osrm.org/table/v1/driving/{coordinates}?annotations=distance"
    response = requests.get(url).json()

    return response['distances']



def solveBestRoute(data, manager, routing):
    
    def distance_callback(to, fro):
        from_node = manager.IndexToNode(fro)
        to_node = manager.IndexToNode(to)
        return data['distanceMatrix'][from_node][to_node]
    callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(callback_index)

    parameters = pywrapcp.DefaultRoutingSearchParameters()
    parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    solution = routing.SolveWithParameters(parameters)

    return solution


# printing solution (copied)
def print_solution(manager, routing, solution,data):
    """Prints the solution."""
    #print('Objective: {} miles'.format(solution.ObjectiveValue()))
    index = routing.Start(0)
    plan_output = 'Route for vehicle 0:\n'
    route_distance = 0
    while not routing.IsEnd(index):
        plan_output += ' {} ->'.format(manager.IndexToNode(index))
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        print(f"Prev: {previous_index}, index: {index}")
        if routing.IsEnd(index):
            route_distance += data['distanceMatrix'][previous_index][3]
            break
        route_distance += data['distanceMatrix'][previous_index][index]
    plan_output += ' {}\n'.format(manager.IndexToNode(index))
    plan_output += 'Distance of the route: {}km \n'.format(route_distance/1000)
    print(plan_output)



main()