import matplotlib.pyplot as plt
import networkx as nx
import osmnx as ox
from collections import deque
from map_snowPlow import map_sector
from package.cout import cost_sp2

def get_edge_lengths(G):
    edge_lengths = {}
    for u, v, key, data in G.edges(keys=True, data=True):
        edge_length = data.get('length', None)
        edge_lengths[(u, v, key)] = edge_length
    return edge_lengths

def find_edge_length_by_key(edge_lengths, u, v, edge_key):
    return edge_lengths.get((u, v, edge_key))

def choose_optimal_sources(G, num_sources=1):
    degree_centrality = nx.degree_centrality(G)
    sorted_nodes = sorted(degree_centrality, key=degree_centrality.get, reverse=True)
    sources = sorted_nodes[:num_sources]
    return sources

def bfs_multisource_colored(G, sources, color_map):
    edge_lengths = get_edge_lengths(G)
    visited_edges = set()
    edge_colors = {}
    queue = deque([(source, None, source, None) for source in sources])  # (current_node, parent_node, source, edge_key)

    while queue:
        node, parent, source, parent_edge_key = queue.popleft()
        
        for neighbor in G.neighbors(node):
            for edge_key in G[node][neighbor]:
                edge_length = find_edge_length_by_key(edge_lengths, node, neighbor, edge_key)
                edge = (node, neighbor, edge_key)
                if edge not in visited_edges:
                    visited_edges.add(edge)
                    queue.append((neighbor, node, source, edge_key))
                    edge_colors[edge] = (color_map[sources.index(source)], edge_length)
                    
    return edge_colors


def draw_graph_with_colored_edges(G, pos, edge_colors):
    plt.figure(figsize=(12, 12))
    
    # Draw nodes and labels
    nx.draw(G, pos, with_labels=False, node_size=30, node_color="black")
    
    # Get the edge list and corresponding colors
    edges = list(edge_colors.keys())
    colors = [edge_colors[edge][0] for edge in edges]
    
    # Draw edges with colors
    nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color=colors, arrows=False)
    
    plt.title('Graph Traversal with Colored Edges')
    plt.show()

# Define sectors and color map
sector1 = "Outremont, Montreal, Quebec, Canada"
sector2 = "Verdun, Montreal, Quebec, Canada"
sector3 = "Anjou, Montreal, Quebec, Canada"
sector4 = "Rivière-des-Prairies-Pointe-aux-Trembles, Montreal, Quebec, Canada"
sector5 = "Le Plateau-Mont-Royal, Montreal, Quebec, Canada"

color_map = [
    "magenta", "darkturquoise",  "red", "yellow","lime", "orange", "purple",
    "pink", "brown", "gray", "olive", "teal",  "maron",
    "gold", "orchid", "seagreen", "salmon", "darkorange", "silver", 
    "darkgoldenrod", "darkslategray", "mediumorchid", "sandybrown", 
    "darkkhaki", "plum", "limegreen", "chocolate", "palevioletred", 
    "rosybrown", "lightcoral", "darkorchid", "indianred", 
    "mediumseagreen", "lightpink", "peru", "green",
]

def find_color(arg, tuple_list):
    for i in range(len(tuple_list)):
        if arg == tuple_list[i][0]:
            return i
    return -1

combined_graph = nx.MultiDiGraph()
total_cost = 0

for i in range(1, 6):
    if i == 1:
        G = map_sector(sector1)
        sources = choose_optimal_sources(G, 1)
    elif i == 2:
        G = map_sector(sector2)
        sources = choose_optimal_sources(G, 3)
    elif i == 3:
        G = map_sector(sector3)
        sources = choose_optimal_sources(G, 3)
    elif i == 4:
        G = map_sector(sector4)
        sources = choose_optimal_sources(G, 5)   
    else:
        G = map_sector(sector5)
        sources = choose_optimal_sources(G, 3)
        
    nodes_data = G.nodes(data=True)
    
    edge_colors = bfs_multisource_colored(G, sources, color_map)
        
    snowplot_distances = []
        
    for value in edge_colors.values():
        color, length = value
        i = find_color(color, snowplot_distances) 
        if i != -1:
            d = snowplot_distances[i][1] + (length if length else 0)
            del snowplot_distances[i]
            snowplot_distances.append((color, d))
        else:
            snowplot_distances.append((color, length if length else 0))
    
    for (color, length) in snowplot_distances:
        print(f"{color}: {length}")
    
    for _,j in snowplot_distances:
        total_cost += cost_sp2(j / 1000)
        
    
    pos = {node: (data['x'], data['y']) for node, data in nodes_data if 'x' in data and 'y' in data}
    # Check for nodes without positions
    for node in G.nodes():
        if node not in pos:
            pos[node] = (0, 0)  # Assign a default position if none is available
    
    draw_graph_with_colored_edges(G, pos, edge_colors)
    
    combined_graph = nx.compose(combined_graph, G)
    
print(f"total_cost: {total_cost}")