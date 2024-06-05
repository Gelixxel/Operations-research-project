import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

def create_subgraph(graph, selected_nodes):
    subgraph = nx.DiGraph()
    subgraph.add_nodes_from(selected_nodes)

    for node in selected_nodes:
        edges = graph.edges(node, data=True)
        for edge in edges:
            target_node = edge[1]
            if target_node in selected_nodes:
                subgraph.add_edge(node, target_node, **edge[2])

    return subgraph

def subGraph(name, range_limit):
    G = ox.graph_from_place(name, network_type='drive')
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

    node_color = ['black'] * len(nodes)
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
            acc = parcours_graph(G, actualNode, range_limit, verif)
            for n in acc:
                verif[nodes.index(n)] = 1
            res.append(acc)
        return res

    sub_graphs = subDiv()

    limit = range_limit // 100
    to_little_graph = [graph for graph in sub_graphs if len(graph) < limit]
    for graph in to_little_graph:
        sub_graphs.remove(graph)

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

    col = 0
    for graph in sub_graphs:
        for n in graph:
            node_color[nodes.index(n)] = colors[col % len(colors)]
        col += 1

    pos = {n: (G.nodes[n]['x'], G.nodes[n]['y']) for n in G.nodes()}
    plt.figure(figsize=(12, 12))
    nx.draw(G, pos, node_size=40, node_color=node_color, edge_color='gray', with_labels=False)
    plt.title(f"Subgraphs for {name}")
    plt.show()
    return sub_graphs

sectors = [
    "Outremont, Montreal, Quebec, Canada",
    "Verdun, Montreal, Quebec, Canada",
    "Anjou, Montreal, Quebec, Canada",
    "Rivière-des-Prairies-Pointe-aux-Trembles, Montreal, Quebec, Canada",
    "Le Plateau-Mont-Royal, Montreal, Quebec, Canada"
]

for sector in sectors:
    print(f"Processing {sector}...")
    # 1000 = 7 color on outremont
    subgraphs = subGraph(sector, 500)
    print(f"Completed {sector}.")
