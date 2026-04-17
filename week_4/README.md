# MCT-454L Mobile Robotics: Week 4 Lab
**Student Name: Shehroz Ali**

**Instructor: Dr. Maria Akram**

# Brief Description
This lab focused on advanced ROS 2 concepts including the Launch system, Rosbag for data logging, and the implementation of automated robot behaviors. The main objectives were to create a Python-based launch package, record and replay topic data using Rosbag, and develop a "Follow-the-Leader" node where a second turtle automatically tracks the first turtle using proportional control. I successfully integrated these components into a single launch file that automates the simulation environment.

# Commands Used
## ROS 2 Launch & Workspace

source /opt/ros/humble/setup.bash — Source the ROS 2 environment.

colcon build --packages-select ShehrozAli_launch_pkg — Build the custom launch package.

source install/setup.bash — Source the local workspace to recognize new nodes and launch files.

ros2 launch ShehrozAli_launch_pkg follow_me.launch.py — Execute the integrated launch file.

# Rosbag Operations

ros2 bag record /turtle1/pose — Record the leader's trajectory data.

ros2 bag play <bag_directory_name> — Playback recorded data to move the turtle.

ros2 bag info <bag_directory_name> — View metadata and recorded topics within a bag file.

# rqt and Visualization

rqt — Open the main rqt GUI.

Plugins → Visualization → Plot: Used to visualize /turtle1/cmd_vel and /turtle2/cmd_vel in real-time.

Plugins → Introspection → Node Graph: Used to verify the connections between the sim, teleop, and follower_logic nodes.

# Manual Node Interaction

ros2 run ShehrozAli_launch_pkg follower_node — Manually start the follower logic node.

ros2 service call /spawn turtlesim/srv/Spawn "{x: 2.0, y: 2.0, name: 'turtle2'}" — Manually spawn the second turtle for testing.

# Problems Faced and Solutions
## Issue 1: Launch File Not Found

Problem: ROS 2 could not locate the launch file even after building the package.

Solution: Modified setup.py to correctly include the launch/ directory in the data_files parameter and performed a clean build using rm -rf build install log.

## Issue 2: Follower Turtle Not Moving

Problem: The second turtle remained stationary despite the leader moving.

Solution: Verified the follower_node was running using ros2 node list and ensured the script had executable permissions using chmod +x.

## Issue 3: Proportional Control Jitter

Problem: The follower turtle would jitter or overlap with the leader when it got too close.

Solution: Implemented a "deadband" distance threshold of 1.0 unit in the Python logic to command a velocity of zero when the goal is reached.

# Reflection
This lab bridged the gap between manual interaction and automated robotics. By developing a Follow-the-Leader behavior, I learned how to implement closed-loop feedback systems where a node processes subscriber data (Pose) to generate publisher commands (Cmd_vel). Recording data with Rosbag highlighted the importance of data logging for post-mission analysis and debugging. Furthermore, the launch system demonstrated how to manage complex multi-node environments efficiently. These skills are fundamental for moving from simple simulations to autonomous mobile robot coordination.
