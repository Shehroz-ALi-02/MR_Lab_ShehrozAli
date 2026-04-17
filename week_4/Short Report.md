# Lab 4 Report: ROS 2 Launch, Rosbag, and Follow-the-Leader

## 1. Approach and Methodology

The objective of this session was to utilize the ROS 2 launch system, record data with Rosbag, and implement a "Follow-the-Leader" behavior.Launch System Configuration: I created a ROS 2 package using the ament_python build type. To ensure the launch files were properly installed and discoverable by colcon, I modified the setup.py file to include the launch directory in the data_files parameter.System Architecture: The setup utilizes a single turtlesim_node. A secondary turtle (turtle2) is added to the same simulator window using a ROS 2 service call to /spawn.Follow-the-Leader Logic: A custom Python node was implemented to act as the "brain" for the second turtle. This node:Subscribes to /turtle1/pose to get the leader's position.Subscribes to /turtle2/pose to track its own position.Calculates the Euclidean distance and heading angle between the two.Publishes linear and angular velocity commands to /turtle2/cmd_vel using a proportional controller to maintain pursuit.

## 2. Findings and ObservationsLaunch Efficiency: 

Using a launch file allowed for the simultaneous execution of the simulator, the follower node, and the teleoperation interface, significantly simplifying the workflow compared to running nodes in individual terminals.Data Recording: While the initial recording focused only on /turtle1/pose , I found that recording commands like /turtle1/cmd_vel is necessary to replay actual movement instructions rather than just observing reported positions.Controller Performance: The proportional controller was effective. I observed that higher angular gains allowed turtle2 to turn more sharply, while a "deadband" (stopping within 1.0 unit) prevented the turtles from overlapping or jittering when they met.

## 3. Modified Launch File

The modified launch file is named turtlesim_launch_multiturtle.py and is located in the launch/ directory of the ShehrozAli_launch_pkg package.It contains:The turtlesim_node to provide the GUI.An Execute Process action to call the /spawn service for the second turtle.The custom follower_node to execute the tracking math.The turtle_teleop_key node to allow manual control of the leader.
    
## 4. Trajectory Data Analysis

Data was captured using ros2 bag record. Below is an analysis of the extracted trajectory data:

Leader Trajectory: The leader turtle followed a stochastic path determined by manual teleop input.

Follower Trajectory: The follower's path shows a direct "pursuit" curve. Unlike the leader, which might make sharp turns, the follower's trajectory is characterized by smooth, constant adjustments toward the leader's current coordinates.

Velocity Correlation: Analysis of the rosbag data shows that the linear velocity of turtle2 is directly proportional to the distance from turtle1. As the gap narrows, the follower slows down, reaching 0 m/s when the leader stops and the follower enters the 1.0-unit proximity zone.

Error Correction: The data confirms that even when the leader makes a 180-degree turn, the follower node successfully recalculates the heading error and publishes the correct angular velocity to rotate and continue the chase
