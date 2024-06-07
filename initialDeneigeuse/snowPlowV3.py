import matplotlib.pyplot as plt
import networkx as nx
import osmnx as ox
from collections import deque
from map_snowPlow import map_sector

def choose_optimal_sources(G, num_sources=1):
    degree_centrality = nx.degree_centrality(G)
    sorted_nodes = sorted(degree_centrality, key=degree_centrality.get, reverse=True)
    sources = sorted_nodes[:num_sources]
    return sources

def bfs_multisource_colored(G, sources, color_map):
    visited_edges = set()
    edge_colors = {}
    queue = deque([(source, None, source, None) for source in sources])  # (current_node, parent_node, source, edge_key)

    while queue:
        node, parent, source, parent_edge_key = queue.popleft()
        
        for neighbor in G.neighbors(node):
            for edge_key in G[node][neighbor]:
                edge = (node, neighbor, edge_key)
                if edge not in visited_edges:
                    visited_edges.add(edge)
                    queue.append((neighbor, node, source, edge_key))
                    edge_colors[edge] = color_map[sources.index(source)]
                    
    return edge_colors

def draw_graph_with_colored_edges(G, pos, edge_colors):
    plt.figure(figsize=(12, 12))
    
    # Draw nodes and labels
    nx.draw(G, pos, with_labels=False, node_size=30, node_color="black")
    
    # Get the edge list and corresponding colors
    edges = list(edge_colors.keys())
    colors = [edge_colors[edge] for edge in edges]
    
    # Draw edges with colors
    nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color=colors, arrows=False)
    
    plt.title('Graph Traversal with Colored Edges')
    plt.show()

# Define sectors and color map
sectors = [
    "Outremont, Montreal, Quebec, Canada",
    "Verdun, Montreal, Quebec, Canada",
    "Anjou, Montreal, Quebec, Canada",
    "Rivière-des-Prairies-Pointe-aux-Trembles, Montreal, Quebec, Canada",
    "Le Plateau-Mont-Royal, Montreal, Quebec, Canada"
]

color_map = [
    "magenta", "darkturquoise",  "red", "yellow","lime", "orange", "purple",
    "pink", "brown", "gray", "olive", "teal",  "maron",
    "gold", "orchid", "seagreen", "salmon", "darkorange", "silver", 
    "darkgoldenrod", "darkslategray", "mediumorchid", "sandybrown", 
    "darkkhaki", "plum", "limegreen", "chocolate", "palevioletred", 
    "rosybrown", "lightcoral", "darkorchid", "indianred", 
    "mediumseagreen", "lightpink", "peru", "green",
]

combined_graph = nx.MultiDiGraph()
for sector in sectors:
    G = map_sector(sector)
    nodes_data = G.nodes(data=True)
    sources = choose_optimal_sources(G, 3)
    
    edge_colors = bfs_multisource_colored(G, sources, color_map)
    
    pos = {node: (data['x'], data['y']) for node, data in nodes_data if 'x' in data and 'y' in data}
    # Check for nodes without positions
    for node in G.nodes():
        if node not in pos:
            pos[node] = (0, 0)  # Assign a default position if none is available
    
    draw_graph_with_colored_edges(G, pos, edge_colors)
    
    combined_graph = nx.compose(combined_graph, G)
    
