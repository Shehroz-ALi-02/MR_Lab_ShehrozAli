# Lab Report: Introduction to Gazebo and RViz 
## 1. Objective
The primary goal of this session was to integrate the TurtleBot3 platform with Gazebo for physics based simulation and RViz for sensor data visualization. The lab focused on performing SLAM (Simultaneous Localization and Mapping) using Cartographer and developing custom ROS 2 nodes to interact with robot odometry and velocity commands.
## 2. Procedure & Task Implementation
**Step 1: Environment & Simulation Setup**

The workspace was configured by exporting the TURTLEBOT3_MODEL as burger. The simulation environment was initialized using the launch file:ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py

**Step 2: SLAM & Visualization**

To enable mapping, the Cartographer node was launched. It was crucial to set use_sim_time:=true to ensure the mapping node synchronized with the Gazebo clock rather than the system clock.RViz Configuration: Added LaserScan, Map, TF, and Odometry plugins.Fixed Frame: Changed the global fixed frame to map to prevent data jumping relative to the robot's starting position.

**Step 3: Navigation and Mapping (Tasks 1, 2, 6, & 7)**

Using the teleop_keyboard node, the robot was manually navigated through the environment.As the robot moved, the LaserScan data (red points) hit walls and populated the occupancy grid in the Map plugin.After exploring the environment, the map was saved using the map_saver_cli.Task 7: The robot was successfully teleoperated back to its origin (0, 0, 0)$ by monitoring the position values in the terminal.

**Step 4: Coordinate Frame Analysis (Task 3)**
The TF (Transform) plugin was used to visualize the robot's internal hierarchy.Observations: The map frame is the global parent. The odom frame tracks movement relative to the start, while base_link represents the physical center of the robot. Sensors like base_scan (LiDAR) are children of the base_link frame.

**Step 5: Data Recording (Task 5)**

A ROS 2 bag was initialized using ros2 bag record -a. This captured all message traffic on topics like /scan, /tf, and /odom. This recording was later played back to verify that the robot's path could be reconstructed in RViz without the Gazebo simulation running.

**Step 6: Custom Node Development (Tasks 8 & 9)**

Two Python scripts were developed to demonstrate programmatic control and feedback:Periodic Publisher: A node using a timer_callback to alternate between a linear velocity of 0.22m/s and 0.0m/s every 2 seconds.Odometry Subscriber: A node that listened to the /odom topic and parsed the Pose data to print the robot's real-time X and Y coordinates to the console.

## 3. Observations on Discrepancies

During the lab, a noticeable discrepancy was observed between the Odometry (calculated by wheel encoders) and the Map position. In Gazebo, virtual "wheel slip" can occur, causing the odometry to drift. However, the SLAM algorithm (Cartographer) corrected this by matching LiDAR scans to the existing map features, demonstrating why sensor fusion is vital for accurate navigation.

## 4. Conclusion

This lab provided a comprehensive understanding of the ROS 2 ecosystem's most powerful tools. Learning to manage the TF tree and synchronize simulation time was a key takeaway. These skills are essential for transitioning from basic teleoperation to autonomous navigation where the robot must "trust" its sensors to understand its place in the world.
