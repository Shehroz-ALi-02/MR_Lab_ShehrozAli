# MCT-454L Mobile Robotics: Week 7 Lab

**Student Name: Shehroz Ali**

**Instructor: Dr. Maria Akram**

# Brief Description

This lab session focused on the autonomous navigation pipeline in ROS 2 using the Nav2 (Navigation 2) stack and the TurtleBot3 Burger. Building upon the mapping work from Lab 5, I successfully loaded a static occupancy grid, localized the robot using AMCL (Adaptive Monte Carlo Localization), and executed multi-waypoint missions. The lab involved setting up the navigation servers (Planner, Controller, and Recoveries), sending goals via RViz, and developing a custom Python node for Dynamic Waypoint Injection. I also analyzed how costmaps (Global and Local) influence path planning and observed autonomous recovery behaviors when faced with dynamic obstacles.

# Commands Used

**Navigation & Localization Setup**

export TURTLEBOT3_MODEL=burger: Set the robot model environment variable.

ros2 launch turtlebot3_navigation2 navigation2.launch.py use_sim_time:=True map:=$HOME/maps/my_map.yaml: Launch the Nav2 stack with the saved map from Lab 5.

**Mission Planning & Execution**

ros2 run turtlebot3_teleop teleop_keyboard: Used for initial movement to help AMCL particles converge.

python3 waypoint_navigator.py: Ran the custom Python node to execute hardcoded waypoints (Task 2).

python3 waypoint_navigator_cmd.py 0.8 0.2 1.0 1.2 -0.5 1.0: Executed Task 3 using command-line arguments for dynamic coordinate input.

**System Inspection**

ros2 topic echo /amcl_pose: Monitored the robot's estimated pose to fill the waypoint table.

ros2 topic list | grep costmap: Identified the topics for global and local costmaps.

ros2 run rqt_graph rqt_graph: Visualized the interaction between the BT Navigator and the recovery servers.

# Problems Faced and Solutions

**Issue 1: Robot Planning Paths Through Walls**

Problem: Initially, the robot tried to drive through obstacles visible on the map.

Solution: Discovered that AMCL localization was not properly initialized. Using the 2D Pose Estimate tool in RViz to align the robot's "particle cloud" with its actual position in Gazebo corrected the localization error.

**Issue 2: Syntax Errors in Waypoint Script**

Problem: The starter code for the Python node had unterminated string literals due to line breaks in the get_logger() calls.

Solution: Re-formatted the Python script to ensure all strings were on single lines and properly indented according to PEP 8 standards.

**Issue 3: Nav2 Action Server Timeouts**

Problem: The waypoint script stayed stuck at "Waiting for FollowWaypoints action server."

Solution: Verified that use_sim_time:=True was set in the Nav2 launch. Without this, the Nav2 servers ignore commands because the ROS clock and Gazebo clock are out of sync.

# Reflection

This lab demonstrated the complete transition from Mapping (Discovery) to Navigation (Execution). The most insightful part was observing the Costmap Inflation Layer; seeing how the robot creates a "buffer zone" around walls explains how autonomous systems maintain safety margins. Implementing the dynamic waypoint script taught me how to interface with ROS 2 Action Servers programmatically, which is more scalable than manual RViz interaction. Finally, Task 5 showed that autonomous navigation is not just about planning a path, but about reacting to the unexpected; the Recovery Behaviors (spinning and re-planning) are what make the system truly "autonomous" rather than just "programmed."
