import matplotlib
import matplotlib.pyplot as plt
import networkx as nx
import osmnx as ox
from package.algorithms import parkourGraphDrone, printInfos
import platform
from package.subGraph import subGraph

# Set the backend explicitly to TkAgg for better compatibility
if platform.system() != "Darwin":
    matplotlib.use('TkAgg')
# print(platform.system())

# first sector
sector1 = "Rivière-des-Prairies-Pointe-aux-Trembles, Montreal, Quebec, Canada"

# Initialize an empty graph
combined_graph = nx.MultiDiGraph()

# Download and combine the street network graphs for the specified sectors
# print(f"Downloading data for {sector}...")
G = ox.graph_from_place(sector1, network_type='drive', simplify=True, retain_all=True)
combined_graph = nx.compose(combined_graph, G)

# Convert the graph to a directed graph
#combined_graph = combined_graph.to_directed()

# Filter dead-end streets
edges_to_remove = []

nodes_data = G.nodes(data=True)
for node, data in nodes_data:
    if (data['street_count'] == 1):
        for u, v, k, data in combined_graph.edges(keys=True, data=True):
            if (node == u):
                edges_to_remove.append((u, v, k))
            if (node == v):
                edges_to_remove.append((u, v, k))

# Remove edges that are dead-ends
combined_graph.remove_edges_from(edges_to_remove)

# Remove isolated nodes
isolated_nodes = list(nx.isolates(combined_graph))
combined_graph.remove_nodes_from(isolated_nodes)

# Calculate the total distance of the graph
total_distance_km = parkourGraphDrone(combined_graph)
print(f"Total distance of the graph: {total_distance_km:.2f} km")

printInfos(combined_graph)

fig, ax = ox.plot_graph(combined_graph, node_size=10, node_color='red', edge_color='w', edge_linewidth=0.5)
# plt.savefig("montreal_combined_graph.png")
plt.show(block=True)

subGraph(combined_graph, 10000)