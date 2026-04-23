# MCT-454L Mobile Robotics: Week 5 Lab
**Student Name: Shehroz Ali**

**Instructor: Dr. Maria Akram**

# Brief Description
This lab session introduced the core simulation and visualization tools used in ROS 2: Gazebo and RViz. Using the TurtleBot3 Burger model, I explored how to bridge the gap between a physics based simulation (Gazebo) and sensor data visualization (RViz). The lab involved launching the turtlebot3_world, performing Simultaneous Localization and Mapping (SLAM) using the Cartographer node, and managing coordinate frames (TF). I also implemented custom ROS 2 nodes for periodic velocity publishing and odometry data monitoring to understand the feedback loop between commands and robot state.

# Commands Used
**Simulation & Visualization Setup**

export TURTLEBOT3_MODEL=burger: Set the environment variable for the specific robot hardware.

ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py: Launch the 3D physics environment.

ros2 launch turtlebot3_cartographer cartographer.launch.py use_sim_time:=true: Start the SLAM node and link it to the simulation clock.

**Mapping & Data Management**

ros2 run turtlebot3_teleop teleop_keyboard: Enable manual control via keyboard.

ros2 bag record -a: Record all active topic data (LiDAR, Odom, TF) into a .mcap or folder for later playback.

ros2 run nav2_map_server map_saver_cli -f ~/maps/my_map: Save the SLAM-generated occupancy grid as a .yaml and .pgm file.

**Topic Inspection**

ros2 topic info /odom: Identify that the message type for odometry is nav_msgs/msg/Odometry.

ros2 run rqt_graph rqt_graph: Visualize the node-topic relationship.

# Problems Faced and Solutions
**Issue 1: Empty Map or "Status: Error" in RViz**

Problem: Upon launching RViz, the map was not visible, and the Global Status showed an error regarding the "Fixed Frame."

Solution: In the RViz "Global Options" panel, I changed the Fixed Frame from base_link to map. Additionally, I ensured that use_sim_time:=true was passed during the Cartographer launch so the sensor data synchronized with Gazebo’s clock.

**Issue 2: Drift in Odometry vs. Visual Position**

Problem: After navigating the robot for several minutes, the "Odometry" arrow in RViz began to drift away from the actual robot position on the map.

Solution: Realized that pure odometry (wheel encoders) accumulates error over time. By enabling the Map and TF plugins, I observed how SLAM corrects this drift by matching LaserScan data to the environment features.

**Issue 3: Map Saver Plugin Failure**

Problem: Running the map_saver_cli command initially failed because the directory /maps did not exist.

Solution: Used mkdir -p ~/maps to create the destination folder and verified that the nav2_map_server package was properly installed.

# Reflection
This lab highlighted the distinction between a robot's Physical World (Gazebo) and its Mental World (RViz). By recording data with ros2 bag, I learned that robotics development often involves playing back sensor data to tune algorithms without needing to re-run the simulation. Understanding the TF (Transform) tree was the most significant takeaway; seeing how odom relates to base_footprint and map explained how robots track their own movement relative to a static world. These tools are the industry standard for debugging real-world autonomous systems.
