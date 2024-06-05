import matplotlib
import matplotlib.pyplot as plt
import networkx as nx
import osmnx as ox
import platform
from package.subGraph import subGraph

# Set the backend explicitly to TkAgg for better compatibility
if platform.system() != "Darwin":
    matplotlib.use('TkAgg')

# Define sectors to process
sectors = [
    "Outremont, Montreal, Quebec, Canada",
    "Verdun, Montreal, Quebec, Canada",
    "Anjou, Montreal, Quebec, Canada",
    "Rivière-des-Prairies-Pointe-aux-Trembles, Montreal, Quebec, Canada",
    "Le Plateau-Mont-Royal, Montreal, Quebec, Canada"
]

# Define colors for each sector's subgraphs
node_colors = [
    "blue", "green", "red", "yellow", "magenta", "orange", "purple",
    "pink", "brown", "gray", "olive", "teal", "lime", "maroon",
    "gold", "orchid", "seagreen", "salmon", "darkorange", "silver",
    "darkgoldenrod", "darkslategray", "mediumorchid", "darkturquoise",
    "sandybrown", "darkkhaki", "plum", "limegreen", "chocolate",
    "palevioletred", "rosybrown", "lightcoral", "darkorchid", "indianred",
    "mediumseagreen", "lightpink", "peru"
]
combined_graph = nx.MultiDiGraph()
color_map = {}
color_index = 0  # Initialize color index to keep track of color assignments

A = 0
range = 7000

# Process each sector
for sector in sectors:
    print(f"Processing {sector}...")
    B = 0
    G = ox.graph_from_place(sector, network_type='drive', simplify=True, retain_all=True)
    
    # Divide the graph into subgraphs
    sub_graphs = subGraph(G, range)  # Adjust range as needed
    
    for sub_nodes in sub_graphs:
        sub_G = G.subgraph(sub_nodes).copy()
        
        # Assign a unique color to each subgraph
        current_color = node_colors[color_index % len(node_colors)]
        for node in sub_G.nodes():
            color_map[node] = current_color
        
        color_index += 1  # Move to the next color
        A += 1
        B += 1
        # Combine the subgraph into the combined graph
        combined_graph = nx.compose(combined_graph, sub_G)
    print(f"{sector} colors : {B}")
    print(f"Completed {sector}.\n")

# Get the color list for all nodes in the combined graph
colors = [color_map.get(node, 'black') for node in combined_graph.nodes()]

print(f"Total colors : {A}")
# Plot the graph with the specified node colors
fig, ax = ox.plot_graph(combined_graph, node_size=20, node_color=colors, edge_linewidth=0.5)
plt.show()
