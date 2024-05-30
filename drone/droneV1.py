import matplotlib.pyplot as plt
import networkx as nx
import osmnx as ox
from package.cout import cost_drone
from geopy.distance import geodesic
import time
# import cProfile
# import pstats

# loading montreal sector
sect = "Montreal, Quebec, Canada"

G = ox.graph_from_place(sect, network_type="drive")

def add_shortest_edges_to_make_eulerian(G, odd_nodes):
    while odd_nodes:
        u = odd_nodes.pop(0)
        min_distance = float('inf')
        closest_node = None

        for v in odd_nodes:
            U = G.nodes[u]['y'], G.nodes[u]['x']
            V = G.nodes[v]['y'], G.nodes[v]['x']
            dist = geodesic(U, V).kilometers
            if dist < min_distance:
                min_distance = dist
                closest_node = v

        if closest_node is not None:
            G.add_edge(u, closest_node, length=min_distance)
            odd_nodes.remove(closest_node)

def calculate_total_distance(G, eulerian_circuit):
    total_distance = 0

    for U, V in eulerian_circuit:
        # Get (lat, lon) of U and V
        U_coords = G.nodes[U]['y'], G.nodes[U]['x']
        V_coords = G.nodes[V]['y'], G.nodes[V]['x']

        # Get Geodesic distance between each point
        edge_distance = geodesic(U_coords, V_coords).kilometers

        # Add the distance
        total_distance += edge_distance

    return total_distance

def Drone_Travel(G):
    start_time = time.time()
    # Convert the directed graph to an undirected graph
    G = G.to_undirected()

    # Identify all odd degree nodes
    odd_nodes = [node for node, degree in G.degree() if degree % 2 != 0]

    # Pair odd degree nodes by adding the shortest links
    add_shortest_edges_to_make_eulerian(G, odd_nodes)

    # Find the node with the highest closeness centrality
    centrality = nx.closeness_centrality(G)
    start_node = max(centrality, key=centrality.get)


    # Find the Eulerian circuit
    eulerian_circuit = list(nx.eulerian_circuit(G, source=start_node))

    # Calculate the total distance traveled
    total_distance = calculate_total_distance(G, eulerian_circuit)
    print("Total Distance Traveled (kilometers):", total_distance)

    # Calculate the cost of the operation
    prix = cost_drone(total_distance)
    print("Price of this operation (in euros):", prix)

    # Extract the node IDs from the eulerian_circuit
    node_ids = [node for node, _ in eulerian_circuit]

    # Compute the execution_time and prints it
    end_time = time.time()
    execution_time = end_time - start_time
    hours, remain = divmod(execution_time, 3600)
    minutes, seconds = divmod(remain, 60)
    print(f"Execution Time: {int(hours):02}hrs {int(minutes):02}mins {int(seconds):02}secs")

    # Plot the graph with the trajectories
    fig, ax = ox.plot_graph(G, show=False, close=False)
    ox.plot_graph_route(G, node_ids, route_linewidth=2, route_color='r', ax=ax)

    return prix, total_distance, node_ids

Drone_Travel(G)

# cProfile.run('Drone_Travel(G)', 'profile_stats')
# p = pstats.Stats('profile_stats')
# p.sort_stats('cumulative').print_stats(10)