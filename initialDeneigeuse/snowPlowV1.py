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
def subGraph(G, range):
    nodes = list(G.nodes)
    def isNotEnd(verif):
        return any(v == 0 for v in verif)

    def parcours_graph(graph, start_node, weight_limit, verif):
        accessible_nodes = set()
        accessible_nodes.add(start_node)
        verif[nodes.index(start_node)] = 1

        def dfs(node, current_weight):
            for neighbor in graph.neighbors(node):
                weight = graph.edges[(node, neighbor, 0)]['length']
                new_weight = current_weight + weight
                if new_weight <= weight_limit and verif[nodes.index(neighbor)] == 0:
                    accessible_nodes.add(neighbor)
                    dfs(neighbor, new_weight)
        dfs(start_node, 0)
        return accessible_nodes

    verif = [0] * len(nodes)
    def findNode(verif):
        for i, v in enumerate(verif):
            if v == 0:
                return i
        return -1

    def subDiv():
        res = []
        while isNotEnd(verif):
            i = findNode(verif)
            verif[i] = 1
            actualNode = nodes[i]
            acc = parcours_graph(G, actualNode, range, verif)
            for n in acc:
                verif[nodes.index(n)] = 1
            res.append(acc)
        return res

    sub_graphs = subDiv()
    limit = range // 100
    to_little_graph = [g for g in sub_graphs if len(g) < limit]
    sub_graphs = [g for g in sub_graphs if len(g) >= limit]

    def findSubGraph(G, graph):
        node = list(graph)[0]
        verif = []
        def dfs(G, graph, node, verif):
            verif.append(node)
            for neighbor in G.neighbors(node):
                if neighbor not in verif:
                    if neighbor not in graph:
                        return neighbor
                    return dfs(G, graph, neighbor, verif)
        return dfs(G, graph, node, verif)

    tmp = len(to_little_graph)
    it = 0
    while it < tmp:
        graph = to_little_graph.pop(0)
        biggerGraphMember = findSubGraph(G, graph)
        if biggerGraphMember is None:
            to_little_graph.append(graph)
            it += 1
            continue
        for g in sub_graphs:
            if biggerGraphMember in g:
                g.update(graph)
                break
        it += 1

    sub_graphs += to_little_graph

    return sub_graphs

# Process each sector
for sector in sectors:
    G = ox.graph_from_place(sector, network_type='drive', simplify=True, retain_all=True)
    
    # Divide the graph into subgraphs
    sub_graphs = subGraph(G, 600)  # Adjust range as needed
    
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
