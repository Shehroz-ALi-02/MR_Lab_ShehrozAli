# ROS 2 Turtlesim and rqt

#Objective
The objective of this exercise was to understand the ROS 2 ecosystem by using Turtlesim for simulation and rqt for graphical interaction with ROS nodes, topics, and services. The task involved calling services, spawning a new turtle, and controlling multiple turtles.

## Procedure
1. First, the Turtlesim node was launched using the ROS 2 command. This opened the simulation window containing a turtle that can move inside the environment.

2. Next, the rqt graphical interface was started to explore the ROS system. Using the Node Graph plugin, the connections between nodes and topics were visualized.

3. The Service Caller plugin in rqt was then used to interact with services:

4. The /reset service was called to reset the simulation.

5. The /spawn service was used to create a second turtle by specifying position values (x, y, theta) and the name turtle2.

6. After spawning the second turtle, its control topic /turtle2/cmd_vel was identified. Velocity commands were sent using ROS 2 topic publishing to move the second turtle independently.

## Observations

1. The /reset service clears the drawing and restarts the simulation.

2. The /spawn service successfully creates a new turtle in the simulator.

3. Each turtle has its own control topic.

4. Commands published to /turtle2/cmd_vel only affect the second turtle.

5. The **rqt** interface helps visualize nodes, topics, and services in real time.


# Conclusion

This exercise demonstrated how ROS 2 nodes, topics, and services interact in a simulation environment. Using Turtlesim and rqt, it was possible to observe system communication, call services through a GUI, and control multiple turtles within the simulation.
