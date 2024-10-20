from ortools.constraint_solver import pywrapcp, routing_enums_pb2


data = {}
data['distance_matrix'] = [
    [0, 9, 56, 12, 15],  # From depot (location 0) to others
    [9, 0, 10, 5, 4],   # Distances from location 1 to others
    [3, 10, 0, 67, 8],   # Distances from location 2 to others
    [42, 5, 6, 0, 7],   # Distances from location 3 to others
    [15, 4, 8, 7, 0]
]
data['requirements'] = [0,3,2,5,1]
data['num_vehicle'] = 1
manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),data['num_vehicle'],0)
routing = pywrapcp.RoutingModel(manager)

def distance_callback(fro, to):
    from_node = manager.IndexToNode(fro)
    to_node = manager.IndexToNode(to)
    return data['distance_matrix'][from_node][to_node]

transit_callback_index = routing.RegisterTransitCallback(distance_callback)
routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

search_parameters = pywrapcp.DefaultRoutingSearchParameters()
search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

solution = routing.SolveWithParameters(search_parameters)
def print_solution(manager, routing, solution):
    """Prints the solution."""
    print('Objective: {} m'.format(solution.ObjectiveValue()))
    index = routing.Start(0)
    plan_output = 'Route for vehicle 0:\n'
    route_distance = 0
    while not routing.IsEnd(index):
        plan_output += ' {} ->'.format(manager.IndexToNode(index))
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += ' {}\n'.format(manager.IndexToNode(index))
    plan_output += 'Distance of the route: {} \n'.format(route_distance)
    print(plan_output)
print_solution(manager, routing, solution)