import matplotlib.pyplot as plt
import networkx as nx
import osmnx as ox

# loading montreal sector
sect = "Montreal, Quebec, Canada"

G = ox.graph_from_place(sect)

# the graph need to be eulerian
G = nx.eulerize(G)

fig, ax = ox.plot_graph(G)
plt.show()
