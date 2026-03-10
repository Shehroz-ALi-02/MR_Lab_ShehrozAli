# MCT-454L Mobile Robotics: Week 1 Lab

**Student Name: Shehroz Ali**
**Instructor: Dr. Maria Akram**

# Brief Description

This lab introduced the use of ROS 2 Humble with Turtlesim and the rqt GUI. The main objectives were to explore nodes, topics, and services using rqt, call services to reset and spawn turtles, and control multiple turtles in the simulation. I successfully spawned a second turtle, controlled it independently, and observed how service calls affect the simulation in real time.

# Commands Used
**ROS 2 Environment & Simulation**

source /opt/ros/humble/setup.bash

ros2 run turtlesim turtlesim_node

ros2 run turtlesim turtle_teleop_key

ros2 topic list

ros2 topic echo /turtle1/pose

ros2 topic pub /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 2.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 1.8}}"

ros2 service call /reset std_srvs/srv/Empty
**rqt and GUI**
rqt

Plugins → Introspection → Node Graph : Visualize nodes and topics

Plugins → Services → Service Caller : Call /reset and /spawn services

**Controlling Turtles**
ros2 topic list                 # List available topics

ros2 topic pub /turtle2/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 2.0}, angular: {z: 1.0}}"

ros2 service call /turtle1/teleport_absolute turtlesim/srv/TeleportAbsolute "{x: 8.0, y: 2.0, theta: 1.57}"

# Problems Faced and Solutions

**Issue 1: Service Not Found**

Problem: Some services did not appear in the rqt Service Caller plugin.

Solution: Verified that the turtlesim node was running and refreshed the service list in rqt.

**Issue 2: Turtle Control Commands Not Working**

Problem: Velocity commands had no effect on the second turtle.

Solution: Confirmed the correct topic /turtle2/cmd_vel using ros2 topic list and ensured proper message format.

**Issue 3: Confusion Between Turtles**

Problem: Commands were sometimes sent to the first turtle by mistake.

Solution: Carefully identified topics for each turtle and tested them separately.

# Reflection

This lab demonstrated how rqt can be used to visualize and interact with ROS 2 nodes, topics, and services. Using Turtlesim, I learned how to Call services to reset or spawn turtles in real time. Control multiple turtles independently using velocity topics. Explore ROS 2’s architecture through a graphical interface. The experience highlighted the importance of understanding topic naming conventions, service parameters, and the relationship between nodes and services in ROS 2. The lab bridged the gap between theoretical ROS 2 concepts and practical interaction within a simulation environment.
