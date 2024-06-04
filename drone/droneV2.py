import matplotlib.pyplot as plt
import networkx as nx
import osmnx as ox
from package.cout import cost_drone
from geopy.distance import geodesic
import time

# loading montreal sector
sect = "Montreal, Quebec, Canada"
G = ox.graph_from_place(sect, network_type="drive", simplify=True)

G = G.to_undirected()

# add odd nodes. The starting and ending nodes can be odd
odd_nodes = [node for node, degree in G.degree() if degree % 2 != 0]

# add edge between odd nodes, the weight is the distance between the nodes
for node in odd_nodes:
    for other_node in odd_nodes:
        if node != other_node:
            G.add_edge(node, other_node, weight=geodesic((G.nodes[node]['y'], G.nodes[node]['x']), (G.nodes[other_node]['y'], G.nodes[other_node]['x'])).m)
            # G.add_edge(node, other_node, weight=geodesic(G.nodes[node], G.nodes[other_node]).m)

# plot the graph
fig, ax = plt.subplots()
nx.draw(G, ax=ax, node_size=10, node_color="skyblue", node_shape="s", font_size=10)
plt.show()
