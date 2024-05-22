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
