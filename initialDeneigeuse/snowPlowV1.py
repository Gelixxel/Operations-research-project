import matplotlib
import matplotlib.pyplot as plt
import networkx as nx
import osmnx as ox
import platform

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

# Function to divide the graph into subgraphs based on range
def subGraph(G, range_limit):
    nodes = list(G.nodes)
    
    colors = [
        "blue", "green", "red", "yellow", "magenta", "orange", "purple",
        "pink", "brown", "gray", "olive", "teal", "lime", "maroon",
        "gold", "orchid", "seagreen", "salmon",
        "darkorange", "silver", "darkgoldenrod", "darkslategray",
        "mediumorchid", "darkturquoise", "sandybrown", "darkkhaki", "plum",
        "limegreen", "chocolate", "palevioletred", "rosybrown",
        "lightcoral", "darkorchid", "indianred", "mediumseagreen", "lightpink", "peru"
    ]

    def parcours_graph(graph, start_node, weight_limit, visited):
        accessible_nodes = set()
        stack = [(start_node, 0)]
        visited.add(start_node)

        while stack:
            node, current_weight = stack.pop()
            accessible_nodes.add(node)
            for neighbor in graph.neighbors(node):
                weight = graph.edges[node, neighbor, 0]['length']
                new_weight = current_weight + weight
                if new_weight <= weight_limit and neighbor not in visited:
                    visited.add(neighbor)
                    stack.append((neighbor, new_weight))

        return accessible_nodes

    visited = set()
    sub_graphs = []

    for node in nodes:
        if node not in visited:
            sub_graph = parcours_graph(G, node, range_limit, visited)
            sub_graphs.append(sub_graph)

    # Remove small subgraphs
    limit = range_limit // 100
    sub_graphs = [graph for graph in sub_graphs if len(graph) >= limit]

    # Combine small subgraphs with larger ones
    to_little_graphs = [graph for graph in sub_graphs if len(graph) < limit]
    sub_graphs = [graph for graph in sub_graphs if len(graph) >= limit]

    while to_little_graphs:
        small_graph = to_little_graphs.pop(0)
        merged = False
        for larger_graph in sub_graphs:
            if any(node in larger_graph for node in small_graph):
                larger_graph.update(small_graph)
                merged = True
                break
        if not merged:
            sub_graphs.append(small_graph)

    # Assign colors to nodes
    node_color = ['black'] * len(nodes)
    col = 0
    for graph in sub_graphs:
        for n in graph:
            node_color[nodes.index(n)] = colors[col % len(colors)]
        col += 1

    pos = {n: (G.nodes[n]['x'], G.nodes[n]['y']) for n in G.nodes()}
    # plt.figure(figsize=(12, 12))
    # nx.draw(G, pos, node_size=40, node_color=node_color, edge_color='gray', with_labels=False)
    # plt.show()
    return sub_graphs

# Process each sector
for sector in sectors:
    G = ox.graph_from_place(sector, network_type='drive', simplify=True, retain_all=True)
    
    # Divide the graph into subgraphs
    sub_graphs = subGraph(G, 10000)  # Adjust range as needed
    
    for sub_nodes in sub_graphs:
        sub_G = G.subgraph(sub_nodes).copy()
        
        # Assign a unique color to each subgraph
        current_color = node_colors[color_index % len(node_colors)]
        for node in sub_G.nodes():
            color_map[node] = current_color
        
        color_index += 1  # Move to the next color
        print(A)
        A += 1
        # Combine the subgraph into the combined graph
        combined_graph = nx.compose(combined_graph, sub_G)

# Get the color list for all nodes in the combined graph
colors = [color_map.get(node, 'black') for node in combined_graph.nodes()]

# Plot the graph with the specified node colors
fig, ax = ox.plot_graph(combined_graph, node_size=10, node_color=colors, edge_linewidth=0.5)
plt.show()
