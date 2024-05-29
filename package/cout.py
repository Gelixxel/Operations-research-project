"""
Calculate the cost of the drone to browse Montreal, considering the distance it browses
parameter: distance which the drone browses
return the total cost of the drone's operation
"""

def cost_drone(distance):
    speed = 60                      # Speed of the drone
    hours = distance / speed        # Number of hours of the drone to browse the distance
    cost = 0.0                      # Initialise the cost
    cost += 0.01 * distance         # Cost per kilometer
    cost += 100 * (hours // 24)     # Fixed cost per day
    if hours % 24 != 0:             # If we begin the last day
        cost += 100                 # Add the last day
    return cost

