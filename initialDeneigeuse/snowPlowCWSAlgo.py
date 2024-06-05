import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import time

start_time = time.time()

# Define the sectors
sectors = [
    "Outremont, Montreal, Canada", 
    "Verdun, Montreal, Canada", 
    "Anjou, Montreal, Canada", 
    "Rivière-des-prairies-pointe-aux-trembles, Montreal, Canada", 
    "Le Plateau-Mont-Royal, Montreal, Canada"
]

# Download the map data for each sector
graphs = [ox.graph_from_place(sector, network_type='drive') for sector in sectors]

# Combine graphs
G = nx.compose_all(graphs)

# Compute and store positions
position = {node: (data['x'], data['y']) for node, data in G.nodes(data=True)}

# Get nodes and edges
nodes, edges = ox.graph_to_gdfs(G, nodes=True, edges=True)

# Calculate the shortest path length between all pairs of nodes
distances = dict(nx.all_pairs_dijkstra_path_length(G, weight='length'))

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
            # Check if the distances exist in the dictionary
            if depot in distances and i in distances[depot] and j in distances[depot] and j in distances[i]:
                saving = distances[depot][i] + distances[depot][j] - distances[i][j]
                savings.append((saving, i, j))
    
    # Sort savings in descending order
    savings.sort(reverse=True, key=lambda x: x[0])

    # Merge routes based on savings
    for saving, i, j in savings:
        route_i = find_route_containing(routes, i)
        route_j = find_route_containing(routes, j)
        
        if route_i != route_j and can_merge(routes, route_i, route_j, vehicle_capacity):
            merge_routes(routes, route_i, route_j)
    
    return list(routes.values())

# Helper functions
def find_route_containing(routes, node):
    for route_key in routes:
        if node in routes[route_key]:
            return route_key
    return None

def can_merge(routes, route_i, route_j, vehicle_capacity):
    # Check if merging route_i and route_j stays within vehicle capacity
    return len(routes[route_i]) + len(routes[route_j]) <= vehicle_capacity

def merge_routes(routes, route_i, route_j):
    routes[route_i].extend(routes[route_j])
    del routes[route_j]

# Assume vehicle capacity
vehicle_capacity = 50  # Example capacity

# Get routes
routes = clarke_wright_savings(distances, vehicle_capacity)

# Compute the execution_time and prints it
end_time = time.time()
execution_time = end_time - start_time
hours, remain = divmod(execution_time, 3600)
minutes, seconds = divmod(remain, 60)
print(f"Execution Time: {int(hours):02}hrs {int(minutes):02}mins {int(seconds):02}secs")

# Create plot
fig, ax = plt.subplots(figsize=(12, 12))

# Plot the base graph
nx.draw(G, pos=position, ax=ax, node_size=10, node_color='black', edge_color='gray', alpha=0.2)

# Plot each route in different colors
colors = ['r', 'g', 'b', 'y', 'c', 'm']
for i, route in enumerate(routes):
    color = colors[i % len(colors)]
    route_edges = [(route[n], route[n + 1]) for n in range(len(route) - 1)]
    nx.draw_networkx_edges(G, pos=position, edgelist=route_edges, edge_color=color, width=2, ax=ax)
    nx.draw_networkx_nodes(G, pos=position, nodelist=route, node_color=color, node_size=50, ax=ax)

plt.show()
