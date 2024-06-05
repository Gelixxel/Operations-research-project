import matplotlib.pyplot as plt
import osmnx as ox
from package.cout import cost_drone, cost_sp1, cost_sp2

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

def recOptimisation(total_distance_km, L, L2):
    # Base case: if the total distance is zero, return the current lists and zero cost
    if total_distance_km <= 0:
        return L, L2, 0
    
    # Initialize minimum cost to a very large value
    min_cost = float('inf')
    best_L = None
    best_L2 = None
    
    # Check all possible distances that SP1 can cover from 0 to total_distance_km
    for distance_sp1 in range(0, int(total_distance_km) + 1):
        distance_sp2 = total_distance_km - distance_sp1
        
        # Calculate the cost for the current split
        cost_sp1_current = cost_sp1(distance_sp1)
        cost_sp2_current = cost_sp2(distance_sp2)
        
        # Total cost for this combination
        total_cost = cost_sp1_current + cost_sp2_current
        
        # If this is the lowest cost so far, update the best solution
        if total_cost < min_cost:
            min_cost = total_cost
            best_L = L + [distance_sp1]
            best_L2 = L2 + [distance_sp2]
    
    return best_L, best_L2, min_cost

def costOptimisation(combined_graph):
    total_distance_km = parkourGraphDrone(combined_graph)
    print(f"Total distance of the graph: {total_distance_km:.2f} km")
    L, L2, total_cost = recOptimisation(total_distance_km, [], [])
    print(f"List of snowplow type 1: {L}")
    print(f"List of snowplow type 2: {L2}")
    print(f"Total cost of the graph traversal: {total_cost:.2f} €")

    # printInfos(combined_graph)
    ox.plot_graph(combined_graph, node_size=10, node_color='red', edge_color='w', edge_linewidth=0.5)
    # plt.savefig("montreal_combined_graph.png")
    plt.show(block=True)