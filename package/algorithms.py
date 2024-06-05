import matplotlib.pyplot as plt
import osmnx as ox
from package.cout import cost_drone, cost_sp1, cost_sp2
import time

def parkourGraphDrone(G):
    # Initialize the total distance
    total_distance_km = 0.0
    
    # Iterate over all edges in the graph
    for u, v, data in G.edges(data=True):
        # Check if the edge has a 'length' attribute
        if 'length' in data:
            # Add the length of the edge to the total distance
            total_distance_km += data['length'] / 1000.0  # Convert meters to kilometers
    
    return total_distance_km

def printInfos(G):
    nodes_data = G.nodes(data=True)
    edges_data = G.edges(data=True)
    # Display the first 5 nodes and their attributes
    print("First 5 nodes:")
    for node, data in list(nodes_data)[:5]:
        print(node, data)

    # Display the first 5 edges and their attributes
    print("\nFirst 5 edges:")
    for u, v, data in list(edges_data)[:5]:
        print(u, v, data)

# def recOptimisation(total_distance_km, L, L2):
#     # Base case: if the total distance is zero, return the current lists and zero cost
#     if total_distance_km <= 0:
#         return L, L2, 0
    
#     # Initialize minimum cost to a very large value
#     min_cost = float('inf')
#     best_L = None
#     best_L2 = None
    
#     # Check all possible distances that SP1 can cover from 0 to total_distance_km
#     for distance_sp1 in range(0, int(total_distance_km) + 1):
#         distance_sp2 = total_distance_km - distance_sp1
        
#         # Calculate the cost for the current split
#         cost_sp1_current = cost_sp1(distance_sp1)
#         cost_sp2_current = cost_sp2(distance_sp2)
        
#         # Total cost for this combination
#         total_cost = cost_sp1_current + cost_sp2_current
        
#         # If this is the lowest cost so far, update the best solution
#         if total_cost < min_cost:
#             min_cost = total_cost
#             best_L = L + [distance_sp1]
#             best_L2 = L2 + [distance_sp2]
    
#     return best_L, best_L2, min_cost

def min_cost_to_clear_distance(total_distance_km, max_hours):
    distance_sp1_8h = 10 * max_hours  # km pouvant être déneigés par une déneigeuse de type I en 8 heures
    distance_sp2_8h = 20 * max_hours  # km pouvant être déneigés par une déneigeuse de type II en 8 heures

    cost_sp1_8h = cost_sp1(distance_sp1_8h)
    cost_sp2_8h = cost_sp2(distance_sp2_8h)

    min_cost = float('inf')
    best_combination = (0, 0)

    for num_sp1 in range(0, int(total_distance_km) // distance_sp1_8h + 1):
        for num_sp2 in range(0, int(total_distance_km) // distance_sp2_8h + 1):
            total_distance_covered = num_sp1 * distance_sp1_8h + num_sp2 * distance_sp2_8h

            if total_distance_covered >= total_distance_km:
                total_cost = num_sp1 * cost_sp1_8h + num_sp2 * cost_sp2_8h

                if total_cost < min_cost:
                    min_cost = total_cost
                    best_combination = (num_sp1, num_sp2)

    return best_combination, min_cost

def costOptimisation(combined_graph, start_time):
    total_distance_km = parkourGraphDrone(combined_graph)
    print(f"Total distance of the graph: {total_distance_km:.2f} km")

    max_hours_values = range(1, 25)
    costs = []
    combinations = []

    for max_hours in max_hours_values:
        combination, total_cost = min_cost_to_clear_distance(total_distance_km, max_hours)
        costs.append(total_cost)
        combinations.append(combination)
        print(f"Max hours: {max_hours}")
        print(f"Combinaison optimale de déneigeuses : Type I = {combination[0]}, Type II = {combination[1]}")
        print(f"Total cost : {total_cost:.2f} €\n")

    
    end_time = time.time()
    execution_time = end_time - start_time
    hours, remain = divmod(execution_time, 3600)
    minutes, seconds = divmod(remain, 60)
    print(f"Execution Time: {int(hours):02}hrs {int(minutes):02}mins {int(seconds):02}secs")

    plt.figure(figsize=(10, 5))
    plt.plot(max_hours_values, costs, marker='o')
    plt.xlabel('Max Hours (h)')
    plt.ylabel('Total Cost (€)')
    plt.title('Time took to clear Montreal snow in function of the cost')
    plt.grid(True)
    plt.show()

    # max_hours = 6

    # combination, total_cost = min_cost_to_clear_distance(total_distance_km, max_hours)

    # print(f"Combinaison optimale de déneigeuses : Type I = {combination[0]}, Type II = {combination[1]}")
    # print(f"Total cost of the graph traversal: {total_cost:.2f} €")

    # # L, L2, total_cost = recOptimisation(total_distance_km, [], [])
    # # print(f"List of snowplow type 1: {L}")
    # # print(f"List of snowplow type 2: {L2}")
    # # print(f"Total cost of the graph traversal: {total_cost:.2f} €")

    # total_time = max_hours * 3600
    # h, r = divmod(total_time, 3600)
    # min, s = divmod(r, 60)
    # print(f"Total duration of the graph traversal for snowplows: {int(h):02}hrs {int(min):02}mins {int(s):02}secs")

    # printInfos(combined_graph)
    ox.plot_graph(combined_graph, node_size=10, node_color='red', edge_color='w', edge_linewidth=0.5)
    # plt.savefig("montreal_combined_graph.png")
    plt.show(block=True)