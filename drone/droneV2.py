import time

import matplotlib.pyplot as plt
import networkx as nx
import osmnx as ox
from geopy.distance import geodesic
from networkx.algorithms import bipartite

from package.cout import cost_drone

# import cProfile
# import pstats

# loading montreal sector
sect = "Montreal, Quebec, Canada"

G = ox.graph_from_place(sect, network_type="drive", simplify=True)

def is_eulerian(G):
    return all(degree % 2 == 0 for _, degree in G.degree())

def find_eulerian_circuit(G, start_node):
    return list(nx.eulerian_circuit(G, source=start_node))

def find_shortest_eulerian_circuit(G, start_node):
    """ Find an Eulerian circuit in graph G starting at node start_node,
        attempting to choose shorter edges first when possible.
    """
    # Ensure the graph is Eulerian
    if not is_eulerian(G):
        raise ValueError("The graph is not Eulerian")

    # The circuit
    circuit = []
    
    # Create a deep copy of the graph so we can modify it
    G = nx.MultiGraph(G)
    
    # Current vertex
    current_vertex = start_node
    
    while True:
        # Get edges from the current vertex
        edges = list(G.edges(current_vertex, data='length'))
        
        if not edges:
            break
        
        # Sort edges by weight (length)
        edges.sort(key=lambda x: x[2])
        
        # Find the edge that is not a bridge, or the shortest if all are bridges
        for u, v, length in edges:
            G.remove_edge(u, v)
            bridge = not nx.is_eulerian(G)
            if not bridge:
                current_vertex = v
                circuit.append((u, v))
                break
            # If removing the edge makes the graph non-Eulerian, add it back
            G.add_edge(u, v, length=length)
        else:
            # If all edges are bridges, choose the shortest
            u, v, length = edges[0]
            G.remove_edge(u, v)
            current_vertex = v
            circuit.append((u, v))

    return circuit

def add_optimal_edges_to_make_eulerian(G, odd_nodes):
    # Create a complete graph of odd-degree nodes
    odd_graph = nx.Graph()
    for i in range(len(odd_nodes)):
        for j in range(i + 1, len(odd_nodes)):
            u, v = odd_nodes[i], odd_nodes[j]
            distance = geodesic((G.nodes[u]['y'], G.nodes[u]['x']), (G.nodes[v]['y'], G.nodes[v]['x'])).kilometers
            odd_graph.add_edge(u, v, weight=distance)

    # Find the minimum weight perfect matching
    min_weight_pairs = nx.algorithms.matching.min_weight_matching(odd_graph, maxcardinality=True, weight='weight')

    # Add the edges to the graph
    for u, v in min_weight_pairs:
        G.add_edge(u, v, length=odd_graph[u][v]['weight'])

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
    G = G.to_undirected()

    # Identify all odd degree nodes
    odd_nodes = [node for node, degree in G.degree() if degree % 2 != 0]

    # Pair odd degree nodes optimally
    add_optimal_edges_to_make_eulerian(G, odd_nodes)

    # Check if the graph is Eulerian
    if not is_eulerian(G):
        return None

    # Find the node with the highest closeness centrality as the start node
    centrality = nx.closeness_centrality(G)
    start_node = max(centrality, key=centrality.get)

    # Find the Eulerian circuit using a heuristic approach
    eulerian_circuit = find_shortest_eulerian_circuit(G, start_node)

    # Calculate the total distance traveled
    total_distance = calculate_total_distance(G, eulerian_circuit)
    print("Total Distance Traveled (kilometers):", total_distance)

    # Calculate the cost of the operation
    prix = cost_drone(total_distance)
    print("Price of this operation (in euros):", prix)

    # Compute the execution time
    end_time = time.time()
    execution_time = end_time - start_time
    hours, remain = divmod(execution_time, 3600)
    minutes, seconds = divmod(remain, 60)
    print(f"Execution Time: {int(hours):02}hrs {int(minutes):02}mins {int(seconds):02}secs")

    return prix, total_distance, execution_time

Drone_Travel(G)

# cProfile.run('Drone_Travel(G)', 'profile_stats')
# p = pstats.Stats('profile_stats')
# p.sort_stats('cumulative').print_stats(10)