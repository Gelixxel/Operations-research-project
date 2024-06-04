import matplotlib
import matplotlib.pyplot as plt
import networkx as nx
import osmnx as ox
import platform
from package.cout import cost_drone, cost_sp1, cost_sp2
from package.algorithms import costOptimisation

if platform.system() != "Darwin":
    matplotlib.use('TkAgg')

# List of sectors to plot
sectors = [
# "Montreal, Quebec, Canada"
######################################
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
    G = ox.graph_from_place(sector, network_type='drive', simplify=True, retain_all=True)
    combined_graph = nx.compose(combined_graph, G)

costOptimisation(combined_graph)