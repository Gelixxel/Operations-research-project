# ERO1-Lyon17

Epita's Lyon17 group ERO1 repository

## Overview
ERO1-Lyon17 is a sophisticated project aimed at optimizing snow removal operations in Montreal, which currently total $165 million annually. Utilizing drones and snowplows, the project leverages advanced algorithms to propose a cost-effective and efficient plan for the city.

## Installation
Clone the repository and install the required Python packages using pip:

```bash
git clone https://github.com/Gelixxel/ERO1-Lyon17.git
cd ERO1-Lyon17
pip3 install -e .
```

## Project Details
This project involves two main components: drones for initial snow level reconnaissance and snowplows for actual snow clearing. The goal is to minimize operational costs while ensuring effective snow clearance, especially when snowfall ranges from 2.5cm to 15cm.

### Drone Operations
The drone is tasked with mapping snow levels across Montreal to prioritize areas for snow removal. The project has evolved through several iterations to optimize the drone's path:

- **First Iteration**: Total city coverage using a model similar to the chinese postman problem.
- **Second Iteration**: Focused coverage using a model similar to the traveling salesman problem to reduce flight distance and time.

### Snowplow Operations
Snowplows are deployed based on the drone's reconnaissance to clear the designated areas efficiently. The operations are modeled to minimize cost and time, balancing between the number of snowplows and total operational hours.

- **First Iteration**: Utilizing the Chinese postman problem to determine optimal routes.
- **Second Iteration**: Implementing the Clarke-Wright Savings algorithm for better routing and cost efficiency.
- **Third Iteration**: A more optimized approach using a modified BFS algorithm to reduce the number of routes and ensure all necessary streets are cleared.

## Running the Solutions
The script allows you to choose various solutions for drone and snow plow simulations:

### Start the Script
Navigate to the project directory and execute:

```bash
./script.sh
```

### Drone Solutions
You can choose from the following drone solutions:
- **First Solution**: (Approx. duration: 1 hour)
- **Second Solution**: (Few minutes)
- **Both Solutions**

### Snow Plow Solutions
You can choose from the following snow plow solutions:
- **First Solution**: Manual node coloring (Few seconds)
- **Second Solution**: Using the CWS algorithm (Few minutes)
- **Third Solution**: Using a BFS type algorithm (Few minutes)
- **All Solutions**
