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

# Assume vehicle capacity
vehicle_capacity = 50  # Example capacity

# Download the map data for each sector
graphs = [ox.graph_from_place(sector, network_type='drive') for sector in sectors]

# Combine graphs
G = nx.compose_all(graphs)

# Compute and store positions
position = {node: (data['x'], data['y']) for node, data in G.nodes(data=True)}

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
            if depot in distances and i in distances[depot] and j in distances[depot] and j in distances[i]:
                saving = distances[depot][i] + distances[depot][j] - distances[i][j]
                savings.append((saving, i, j))
    
    # Sort savings in descending order
    savings.sort(reverse=True, key=lambda x: x[0])

    # Merge routes based on savings
    for saving, i, j in savings:
        if can_merge(routes, i, j, vehicle_capacity):
            merge_routes(routes, i, j)

    # Flatten routes
    new_routes = []
    seen = set()
    for route in routes.values():
        if route[0] not in seen:
            new_routes.append(route)
            seen.update(route)
    return new_routes

# Assuming can_merge and merge_routes are properly implemented
def can_merge(routes, i, j, vehicle_capacity):
    route_i = find_route_containing(routes, i)
    route_j = find_route_containing(routes, j)
    if route_i != route_j:
        return len(routes[route_i]) + len(routes[route_j]) <= vehicle_capacity
    return False

def merge_routes(routes, i, j):
    route_i = find_route_containing(routes, i)
    route_j = find_route_containing(routes, j)
    if route_i != route_j:
        routes[route_i].extend(routes[route_j])
        del routes[route_j]

def find_route_containing(routes, node):
    for route_key, route in routes.items():
        if node in route:
            return route_key
    return None

# List to hold all sector routes
all_sector_routes = []

for sector in sectors:
    try:
        # Retrieve and simplify each sector's graph
        graph = ox.graph_from_place(sector, network_type='drive')
        
        # Compute and store positions
        position = {node: (data['x'], data['y']) for node, data in G.nodes(data=True)}
        
        # Calculate the shortest path length between all pairs of nodes
        distances = dict(nx.all_pairs_dijkstra_path_length(G, weight='length'))

        # Apply Clarke-Wright algorithm to this sector's graph
        routes = clarke_wright_savings(distances, vehicle_capacity)
        
        # Store routes for later plotting
        all_sector_routes.append((G, position, routes))

    except Exception as e:
        print(f"Failed to process {sector}: {e}")


# Compute the execution_time and prints it
end_time = time.time()
execution_time = end_time - start_time
hours, remain = divmod(execution_time, 3600)
minutes, seconds = divmod(remain, 60)
print(f"Execution Time: {int(hours):02}hrs {int(minutes):02}mins {int(seconds):02}secs")

# Visualization
fig, axs = plt.subplots(len(all_sector_routes), 1, figsize=(12, 12 * len(all_sector_routes)))

if len(all_sector_routes) == 1:  # Adjust in case there's only one subplot
    axs = [axs]

for ax, (G, position, routes) in zip(axs, all_sector_routes):
    nx.draw(G, pos=position, ax=ax, node_size=10, node_color='black', edge_color='gray', alpha=0.2)
    colors = ['r', 'g', 'b', 'y', 'c', 'm']
    for i, route in enumerate(routes):
        color = colors[i % len(colors)]
        route_edges = [(route[n], route[n + 1]) for n in range(len(route) - 1)]
        nx.draw_networkx_edges(G, pos=position, edgelist=route_edges, edge_color=color, width=2, ax=ax)
        nx.draw_networkx_nodes(G, pos=position, nodelist=route, node_color=color, node_size=50, ax=ax)

plt.tight_layout()
plt.show()