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

def cost_sp1(distance):
    speed = 10                      # Speed of the snowplow
    hours = distance / speed        # Number of hours of the snowplow to browse the distance
    cost = 0.0                      # Initialise the cost
    cost += 1.1 * distance          # Cost per kilometer
    cost += 500 * (hours // 24)     # Fixed cost per day
    if hours % 24 != 0:             # If we begin the last day
        cost += 500                 # Add the last day
    if hours > 8:                   # Add the hourly cost
        cost += 8 * 1.1
        hours -= 8
        cost += 1.3 * hours
    else:
        cost += 1.1 * hours
    return cost

def cost_sp2(distance):
    speed = 20                      # Speed of the snowplow
    hours = distance / speed        # Number of hours of the drone to snowplow the distance
    cost = 0.0                      # Initialise the cost
    cost += 1.3 * distance          # Cost per kilometer
    cost += 800 * (hours // 24)     # Fixed cost per day
    if hours % 24 != 0:             # If we begin the last day
        cost += 800                 # Add the last day
    if hours > 8:                   # Add the hourly cost
        cost += 8 * 1.3
        hours -= 8
        cost += 1.5 * hours
    else:
        cost += 1.3 * hours
    return cost