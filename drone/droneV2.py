import platform
import time
from statistics import median

import matplotlib
import matplotlib.pyplot as plt
import networkx as nx
import osmnx as ox
from geopy.distance import geodesic

if platform.system() != "Darwin":
    matplotlib.use('TkAgg')

# loading montreal sector
sectors = [
    "Ahuntsic-Cartierville, Montreal, Quebec, Canada",
    "Anjou, Montreal, Quebec, Canada",
    "Côte-des-Neiges–Notre-Dame-de-Grâce, Montreal, Quebec, Canada",
    "LaSalle, Montreal, Quebec, Canada",
    "Lachine, Montreal, Quebec, Canada",
    "Le Plateau-Mont-Royal, Montreal, Quebec, Canada",
    "Le Sud-Ouest, Montreal, Quebec, Canada",
    "L’Île-Bizard–Sainte-Geneviève, Montreal, Quebec, Canada",
    "Mercier–Hochelaga-Maisonneuve, Montreal, Quebec, Canada",
    "Montréal-Nord, Montreal, Quebec, Canada",
    "Outremont, Montreal, Quebec, Canada",
    "Pierrefonds-Roxboro, Montreal, Quebec, Canada",
    "Rivière-des-Prairies–Pointe-aux-Trembles, Montreal, Quebec, Canada",
    "Rosemont–La Petite-Patrie, Montreal, Quebec, Canada",
    "Saint-Laurent, Montreal, Quebec, Canada",
    "Saint-Léonard, Montreal, Quebec, Canada",
    "Verdun, Montreal, Quebec, Canada",
    "Ville-Marie, Montreal, Quebec, Canada",
    "Villeray–Saint-Michel–Parc-Extension, Montreal, Quebec, Canada"
]

# Initialize an empty graph
combined_graph = nx.MultiDiGraph()

centralized_nodes = []

# Download and combine the street network graphs for the specified sectors and add the closest node from centrality to the centralized_nodes list
for sector in sectors:
    G = ox.graph_from_place(sector, network_type="drive", simplify=True, retain_all=True)
    combined_graph = nx.compose(combined_graph, G)
    centrality = nx.closeness_centrality(G)
    central_node = max(centrality, key=centrality.get)
    centralized_nodes.append(central_node)

# Dictionary to store shortest paths
shortest_paths = {}

# Function to find alternative nodes with paths
def find_alternative_nodes(G, node1, node2):
    neighbors1 = list(G.neighbors(node1))
    neighbors2 = list(G.neighbors(node2))
    
    for alt_node1 in neighbors1:
        for alt_node2 in neighbors2:
            try:
                nx.dijkstra_path(G, alt_node1, alt_node2)
                return alt_node1, alt_node2
            except nx.NetworkXNoPath:
                continue
    return None, None

# Compute the shortest path for each pair of centralized nodes and add it to the shortest_paths dictionary
for i, node1 in enumerate(centralized_nodes):
    for node2 in centralized_nodes[i+1:]:
        try:
            path = nx.dijkstra_path(combined_graph, node1, node2)
            shortest_paths[(node1, node2)] = path
        except nx.NetworkXNoPath:
            print(f"No path between {node1} and {node2}, finding alternative nodes.")
            alt_node1, alt_node2 = find_alternative_nodes(combined_graph, node1, node2)
            if alt_node1 and alt_node2:
                try:
                    path = nx.dijkstra_path(combined_graph, alt_node1, alt_node2)
                    shortest_paths[(alt_node1, alt_node2)] = path
                except nx.NetworkXNoPath:
                    print(f"No alternative path found between {alt_node1} and {alt_node2}, skipping.")
            else:
                print(f"No alternative nodes found for {node1} or {node2}, skipping.")

# Function to calculate the total distance of a path
def calculate_total_distance(G, path):
    total_distance = 0
    for i in range(len(path) - 1):
        U = G.nodes[path[i]]['y'], G.nodes[path[i]]['x']
        V = G.nodes[path[i+1]]['y'], G.nodes[path[i+1]]['x']
        total_distance += geodesic(U, V).kilometers
    return total_distance

# Calculate the total distance for each shortest path and store it in a list
distances = [calculate_total_distance(combined_graph, path) for path in shortest_paths.values()]

# Plot the montreal map with the shortest path between nodes
fig, ax = ox.plot_graph(combined_graph, show=False, close=False)
for path in shortest_paths.values():
    if all(node in combined_graph.nodes for node in path):
        ox.plot_graph_route(combined_graph, path, route_linewidth=2, route_color='r', ax=ax)
plt.show()