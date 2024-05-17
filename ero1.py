import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

# List of sectors to plot
sectors = [
    "Outremont, Montreal, Quebec, Canada",
    "Verdun, Montreal, Quebec, Canada",
    "Anjou, Montreal, Quebec, Canada",
    "Rivière-des-Prairies-Pointe-aux-Trembles, Montreal, Quebec, Canada",
    "Le Plateau-Mont-Royal, Montreal, Quebec, Canada"
]

# Initialize an empty graph
combined_graph = nx.MultiDiGraph()

# Download and combine the street network graphs for the specified sectors
for sector in sectors:
    # print(f"Downloading data for {sector}...")
    G = ox.graph_from_place(sector, network_type='drive_service')
    combined_graph = nx.compose(combined_graph, G)

# Convert the graph to a directed graph
# combined_graph = combined_graph.to_directed()

# filtered graph by reads

# road_types = ['primary', 'secondary', 'tertiary']
# edges_to_remove = [(u, v, k) for u, v, k, data in combined_graph.edges(keys=True, data=True)
#                    if data['highway'] not in road_types]

# Remove edges that are not of the specified road types
# combined_graph.remove_edges_from(edges_to_remove)
# Remove isolated nodes
# isolated_nodes = list(nx.isolates(combined_graph))
# combined_graph.remove_nodes_from(isolated_nodes)

fig, ax = ox.plot_graph(combined_graph, node_size=10, node_color='red', edge_color='w', edge_linewidth=0.5)
# plt.savefig("montreal_combined_graph.png")

plt.show()
