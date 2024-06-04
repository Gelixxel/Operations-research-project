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

# Define the sectors
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

# Download the entire Montreal street network
print("Downloading the street network for Montreal...")
montreal_graph = ox.graph_from_place("Montreal, Quebec, Canada", network_type='drive')
print("Downloaded the street network for Montreal.")

# Calculate the centrality for each node and find the most central node for each sector
central_nodes = []
for sector in sectors:
    sector_graph = ox.graph_from_place(sector, network_type='drive')
    centrality = nx.betweenness_centrality(sector_graph)
    most_central_node = max(centrality, key=centrality.get)
    central_nodes.append(most_central_node)
    print(f"Central node for sector {sector} is {most_central_node}")

# Compute the shortest path for each pair of centralized nodes and connect the last node to the first
all_paths = []
for i in range(len(central_nodes)):
    source = central_nodes[i]
    target = central_nodes[(i + 1) % len(central_nodes)]  # Connect last node back to the first node
    if nx.has_path(montreal_graph, source, target):  # Check if path exists in the Montreal graph
        shortest_path = nx.shortest_path(montreal_graph, source=source, target=target, weight='length')
        all_paths.append(shortest_path)
        print(f"Shortest path between {source} and {target} is {shortest_path}")
    else:
        print(f"No path between {source} and {target}.")

# Plot the Montreal map with all shortest paths
print("Plotting the Montreal map with the shortest path between each pair of nodes in red...")
fig, ax = ox.plot_graph(montreal_graph, node_size=10, edge_color='gray', show=False, close=False)

# Plot all paths in red
ox.plot_graph_routes(montreal_graph, routes=all_paths, route_linewidth=2, route_color='red', ax=ax, orig_dest_node_size=0)

plt.show()
