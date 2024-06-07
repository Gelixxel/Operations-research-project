#!/bin/bash

echo "Our project requires Python and pip installed on your system."
echo "Please make sure you have them installed before running the project."
echo "You can install them by running the following commands:"
echo "sudo apt-get update && sudo apt-get install python3 python3-pip"

echo "Installing required packages..."
pip3 install -e .

echo "Which solution would you like to run for the drone? (the first take about an hour to run, a few minutes for the second)"
echo "1) First Solution"
echo "2) Second Solution"
echo "3) Both Solutions"
read -p "Enter the number of your choice: " choice1

echo "Which solution would you like to run for the snowPlow?"
echo "First solution is coloring the node 'by hand', second solution is using the CWS algorithm, third solution is showind the paths."
echo "1) First Solution"
echo "2) Second Solution"
echo "3) Third Solution"
echo "4) All Solutions"
read -p "Enter the number of your choice: " choice2


run_drone_first_solution() {
    echo "Running First Drone Solution..."
    python3 drone/droneV1.py
}


run_drone_second_solution() {
    echo "Running Second Drone Solution..."
    python3 drone/droneV2.py
}


run_snowPlow_first_solution() {
    echo "Running First SnowPlow Solution..."
    python3 initialDeneigeuse/snowPlowV1.py
}


run_snowPlow_second_solution() {
    echo "Running Second SnowPlow Solution..."
    python3 initialDeneigeuse/snowPlowCWSAlgo.py
}


run_snowPlow_third_solution() {
    echo "Running Third SnowPlow Solution..."
    python3 initialDeneigeuse/snowPlowV3.py
}

case $choice1 in
    1)
        run_drone_first_solution
        ;;
    2)
        run_drone_second_solution
        ;;
    3)
        run_drone_first_solution
        run_drone_second_solution
        ;;
    *)
        echo "Invalid choice for drone solution. Please run the script again and select a valid option."
        exit 1
        ;;
esac

case $choice2 in
    1)
        run_snowPlow_first_solution
        ;;
    2)
        run_snowPlow_second_solution
        ;;
    3)
        run_snowPlow_third_solution
        ;;
    4)
        run_snowPlow_first_solution
        run_snowPlow_second_solution
        run_snowPlow_third_solution
        ;;
    *)
        echo "Invalid choice for snowPlow solution. Please run the script again and select a valid option."
        exit 1
        ;;
esac

echo "All selected solutions have been executed."
