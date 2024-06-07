import matplotlib
import matplotlib.pyplot as plt
import networkx as nx
import osmnx as ox
import platform 
from collections import deque
from map_snowPlow import map_sector

def choose_optimal_sources(G, num_sources=1):
    degree_centrality = nx.degree_centrality(G)
    sorted_nodes = sorted(degree_centrality, key=degree_centrality.get, reverse=True)
    sources = sorted_nodes[:num_sources]
    
    return sources

def bfs_multisource_colored(G, sources, color_map):
    visited = set()
    edge_colors = {}
    queue = deque([(source, None, source) for source in sources])
    
    while queue:
        node, parent, source = queue.popleft()
        if node not in visited:
            visited.add(node)
            neighbors = set(G.neighbors(node)) - visited
            
            for neighbor in neighbors:
                queue.append((neighbor, node, source))
                
            if parent is not None:
                for key in G[parent][node]:
                    edge_colors[(parent, node, key)] = color_map[sources.index(source)]
    
    return edge_colors


def draw_graph_with_colored_edges(G, pos, edge_colors):
    plt.figure(figsize=(12, 12))
    # Draw nodes and labels
    nx.draw(G, pos, with_labels=False, node_size=40, node_color="black", font_size=8, font_color='black', connectionstyle='arc3,rad=0.1', arrows=True, arrowstyle='-|>', arrowsize=20)
    
    # Get the edge list and corresponding colors
    edges = list(edge_colors.keys())
    colors = [edge_colors[edge] for edge in edges]
    
    # Draw edges with colors
    nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color=colors, connectionstyle='arc3,rad=0.1', arrows=True, arrowstyle='-|>', arrowsize=20)
    
    # Draw nodes and la
    plt.title('Graph Traversal with Colored Edges')
    plt.show()

# first sector
sector1 = "Outremont, Montreal, Quebec, Canada"

G1 = map_sector(sector1)

nodes_data = G1.nodes(data=True)
print("First 5 nodes:")
for node, data in list(nodes_data)[:5]:
    print(node, data)
        
sources = choose_optimal_sources(G1, 3)


color_map = [
        "magenta", "darkturquoise", "green", "red", "yellow", "orange", "purple",
        "pink", "brown", "gray", "olive", "teal", "lime", "maroon",
        "gold", "orchid", "seagreen", "salmon",
        "darkorange", "silver", "darkgoldenrod", "darkslategray",
        "mediumorchid", "sandybrown", "darkkhaki", "plum",
        "limegreen", "chocolate", "palevioletred", "rosybrown",
        "lightcoral", "darkorchid", "indianred", "mediumseagreen", "lightpink", "peru"
    ]

# Perform BFS with colored edges
edge_colors = bfs_multisource_colored(G1, sources, color_map)
pos = nx.spring_layout(G1)

# Draw the graph with colored edges
draw_graph_with_colored_edges(G1, pos, edge_colors)
