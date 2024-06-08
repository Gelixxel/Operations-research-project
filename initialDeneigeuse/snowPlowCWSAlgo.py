import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import time

from package.algorithms import parkourGraphDrone
from package.cout import cost_sp1, cost_sp2

start_time = time.time()

# Define the sectors
sectors = [
    "Outremont, Montreal, Canada",
    "Verdun, Montreal, Canada",
    "Anjou, Montreal, Canada",
    "Rivière-des-prairies-pointe-aux-trembles, Montreal, Canada",
    "Le Plateau-Mont-Royal, Montreal, Canada"
]

max_sp1 = 2

# Assume vehicle capacity
vehicle_capacity = 300

# List to hold all sector routes
all_sector_routes = []

combined_graph = nx.MultiDiGraph()

# Function definitions for Clarke-Wright algorithm
def clarke_wright_savings(distances, vehicle_capacity):
    # Initialize routes with each node as a separate route
    routes = {node: [node] for node in distances}
    savings = []

    # Use the first node as the depot
    depot = list(distances.keys())[0]

    # Calculate savings for all pairs of nodes
    for i in distances:
        if i == depot:
            continue
        for j in distances[i]:
            if j == depot or i == j:
                continue
            if depot in distances and i in distances[depot] and j in distances[depot] and j in distances[i]:
                saving = distances[depot][i] + distances[depot][j] - distances[i][j]
                savings.append((saving, i, j))
    
    # Sort savings in descending order
    savings.sort(reverse=True, key=lambda x: x[0])

    # Merge routes based on savings
    for saving, i, j in savings:
        if can_merge(routes, i, j, vehicle_capacity):
            merge_routes(routes, i, j)

    return [routes[key] for key in sorted(routes)]

def can_merge(routes, i, j, vehicle_capacity):
    route_i = find_route_containing(routes, i)
    route_j = find_route_containing(routes, j)
    if route_i != route_j:
        return len(routes[route_i]) + len(routes[route_j]) <= vehicle_capacity
    return False

def merge_routes(routes, i, j):
    route_i = find_route_containing(routes, i)
    route_j = find_route_containing(routes, j)
    routes[route_i].extend(routes[route_j])
    del routes[route_j]

def find_route_containing(routes, node):
    for route_key, route in routes.items():
        if node in route:
            return route_key
    return None

total_distance = 0
total_cost = 0

for sector in sectors:
    try:
        print(f"Processing {sector}...")
        # Retrieve and simplify each sector's graph
        G = ox.graph_from_place(sector, network_type='drive')
        
        # Compute and store positions
        position = {node: (data['x'], data['y']) for node, data in G.nodes(data=True)}
        
        # Calculate the shortest path length between all pairs of nodes
        distances = dict(nx.all_pairs_dijkstra_path_length(G, weight='length'))

        # Apply Clarke-Wright algorithm to this sector's graph
        routes = clarke_wright_savings(distances, vehicle_capacity)

        # Combine the subgraph into the combined graph
        combined_graph = nx.compose(combined_graph, G)
        
        # Store routes for later plotting
        all_sector_routes.append((G, position, routes))

        sector_distance = parkourGraphDrone(G)
        snowplow_count = 0
        for _, route in enumerate(routes):
            if (len(route) == 1):
                continue
            snowplow_count += 1
        if sector_distance < 80:
            sector_cost = cost_sp1(sector_distance)
        elif (sector_distance % 160) <= 80 & max_sp1 > 0:
            sector_cost = cost_sp2((sector_distance - (sector_distance % 160)) / (snowplow_count - 1)) * (snowplow_count - 1) + cost_sp1(sector_distance % 160)
            max_sp1 -= 1
        else:
            sector_cost = cost_sp2(sector_distance / snowplow_count) * snowplow_count
        total_distance += sector_distance
        total_cost += sector_cost
        print(f"Sector distance {sector_distance} km")
        print(f"Total cost of the operation in this sector {sector_cost} €")
        print(f"Completed {sector}.\n")

    except Exception as e:
        print(f"Failed to process {sector}: {e}")

# Compute the execution time and prints it
end_time = time.time()
execution_time = end_time - start_time
hours, remain = divmod(execution_time, 3600)
minutes, seconds = divmod(remain, 60)
print(f"Total distance {total_distance} km")
print(f"Total cost of the operation {total_cost} €")
print(f"Execution Time: {int(hours):02}hrs {int(minutes):02}mins {int(seconds):02}secs")

# Visualization on a single plot
fig, ax = plt.subplots(1, 1, figsize=(6, 10))
nb = 0
for G, position, routes in all_sector_routes:
    # Draw each graph on the same subplot
    nx.draw(G, pos=position, ax=ax, node_size=10, node_color='black', edge_color='gray', alpha=0.2)
    colors = [
        "green", "teal", "orangered", "slateblue", "lightseagreen", "deeppink",
        "aquamarine", "royalblue", "gold", "darkviolet", "pink", "yellowgreen",
        "springgreen", "steelblue", "darkorange", "indigo", "crimson",
        "chartreuse", "red", "navy", "magenta", "hotpink",
        "turquoise", "lavender", "yellow", "darkmagenta", "lightpink"
        "seagreen", "deepskyblue", "chocolate", "rebeccapurple",
    ]
    for _, route in enumerate(routes):
        if (len(route) == 1):
            continue
        color = colors[nb % len(colors)]
        nb += 1
        route_edges = [(route[n], route[n + 1]) for n in range(len(route) - 1)]
        nx.draw_networkx_edges(G, pos=position, edgelist=route_edges, edge_color=color, width=1, ax=ax)
        nx.draw_networkx_nodes(G, pos=position, nodelist=route, node_color=color, node_size=20, ax=ax)

print(f"Nb colors : {nb}")
plt.tight_layout()
plt.show()
# fig.savefig("snowPlowV2.pdf", dpi=300, format='pdf')
