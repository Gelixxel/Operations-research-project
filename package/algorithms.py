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
    return L, L2

def costOptimisation(combined_graph):
    total_distance_km = parkourGraphDrone(combined_graph)
    print(f"Total distance of the graph: {total_distance_km:.2f} km")
    L, L2 = recOptimisation(total_distance_km, [], [])
    print(f"List of snowplow type 1: {L}")
    print(f"List of snowplow type 2: {L2}")
    total_cost = 0
    print(f"Total cost of the graph traversal: {total_cost:.2f} €")

    # printInfos(combined_graph)
    ox.plot_graph(combined_graph, node_size=10, node_color='red', edge_color='w', edge_linewidth=0.5)
    # plt.savefig("montreal_combined_graph.png")
    plt.show(block=True)