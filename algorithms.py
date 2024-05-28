import networkx as nx
import osmnx as ox


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