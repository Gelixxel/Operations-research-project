import platform
import time
from statistics import median

import matplotlib
import matplotlib.pyplot as plt
import networkx as nx
import osmnx as ox
from geopy.distance import geodesic

from package.cout import cost_drone

if platform.system() != "Darwin":
    matplotlib.use('TkAgg')

# Define the sectors
sectors = [
    "Rivière-des-Prairies–Pointe-aux-Trembles, Montreal, Quebec, Canada",
    "Montréal-Nord, Montreal, Quebec, Canada",
    "Saint-Léonard, Montreal, Quebec, Canada",
    "Anjou, Montreal, Quebec, Canada",
    "Mercier–Hochelaga-Maisonneuve, Montreal, Quebec, Canada",
    "Rosemont–La Petite-Patrie, Montreal, Quebec, Canada",
    "Villeray–Saint-Michel–Parc-Extension, Montreal, Quebec, Canada",
    "Ahuntsic-Cartierville, Montreal, Quebec, Canada",
    "Le Plateau-Mont-Royal, Montreal, Quebec, Canada",
    "Ville-Marie, Montreal, Quebec, Canada",
    "Outremont, Montreal, Quebec, Canada",
    "Côte-des-Neiges–Notre-Dame-de-Grâce, Montreal, Quebec, Canada",
    "Le Sud-Ouest, Montreal, Quebec, Canada",
    "Verdun, Montreal, Quebec, Canada",
    "LaSalle, Montreal, Quebec, Canada",
    "Lachine, Montreal, Quebec, Canada",
    "Saint-Laurent, Montreal, Quebec, Canada",
    "Pierrefonds-Roxboro, Montreal, Quebec, Canada",
    "L’Île-Bizard–Sainte-Geneviève, Montreal, Quebec, Canada"
]

# Function to calculate the total distance of all paths
def calculate_total_distance(graph, paths):
    total_distance = 0
    for path in paths:
        for i in range(len(path) - 1):
            edge_data = graph.get_edge_data(path[i], path[i + 1])
            # The distance might be stored under different keys; checking common possibilities
            distance = edge_data[0].get('length', 0)  # 0th element assuming graph is multi-edge
            total_distance += distance
    return total_distance / 1000  # Convert meters to kilometers

start_time = time.time()

# Download the entire Montreal street network
print("Downloading the street network for Montreal...")
montreal_graph = ox.graph_from_place("Montreal, Quebec, Canada", network_type='drive')
print("Downloaded the street network for Montreal.")

montreal_graph = montreal_graph.to_undirected()

# Calculate the centrality for each node and find the most central node for each sector
central_nodes = []
for sector in sectors:
    sector_graph = ox.graph_from_place(sector, network_type='drive')
    centrality = nx.betweenness_centrality(sector_graph)
    most_central_node = max(centrality, key=centrality.get)
    central_nodes.append(most_central_node)
    # print(f"Central node for sector {sector} is {most_central_node}")

# Compute the shortest path for each pair of centralized nodes and connect the last node to the first
all_paths = []
for i in range(len(central_nodes) - 1):
    source = central_nodes[i]
    target = central_nodes[(i + 1) % len(central_nodes)]  # Connect last node back to the first node
    if nx.has_path(montreal_graph, source, target):  # Check if path exists in the Montreal graph
        shortest_path = nx.shortest_path(montreal_graph, source=source, target=target, weight='length')
        all_paths.append(shortest_path)
        # print(f"Shortest path between {source} and {target} is {shortest_path}")
    else:
        print(f"No path between {source} and {target}.")

# Calculate the total distance traveled
total_distance = calculate_total_distance(montreal_graph, all_paths)
print("Total Distance Traveled (kilometers):", total_distance)

# Calculate the cost of the operation
prix = cost_drone(total_distance)
print("Price of this operation (in euros):", prix)

# Compute the execution_time and prints it
end_time = time.time()
execution_time = end_time - start_time
hours, remain = divmod(execution_time, 3600)
minutes, seconds = divmod(remain, 60)
print(f"Execution Time: {int(hours):02}hrs {int(minutes):02}mins {int(seconds):02}secs")

# Plot the Montreal map with all shortest paths
print("Plotting the Montreal map with the shortest path between each pair of nodes in red...")
fig, ax = ox.plot_graph(montreal_graph, node_size=10, edge_color='gray', show=False, close=False)

# Plot all paths in red
ox.plot_graph_routes(montreal_graph, routes=all_paths, route_linewidth=1, route_color='red', ax=ax, orig_dest_node_size=0)

plt.show()
