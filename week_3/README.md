# MCT-454L Mobile Robotics: Week 3 Lab

**Student Name: Shehroz Ali**

**Instructor: Dr. Maria Akram**

# Brief Description

This lab focused on advanced ROS 2 node development to control multiple agents and implement closed-loop feedback systems. The main objectives were to create a ROS 2 Python package and write scripts to move a turtle in circular and triangular patterns. I successfully implemented a multi-turtle coordination system where three turtles (drawing a Pentagon, Hexagon, and Rectangle) operated simultaneously without path intersections. Additionally, I developed an interactive "Go-to-Goal" controller that utilizes the /pose topic to move the turtle to specific user-defined coordinates.

# Commands Used
**Workspace & Package Setup**

mkdir -p ~/ros2_ws/src : Create the workspace directory structure.

colcon build : Compile the ROS 2 workspace and packages.

source install/setup.bash : Overlay the workspace on the environment.

ros2 pkg create --build-type ament_python --dependencies rclpy turtlesim my_turtle_package : Create a new Python-based ROS 2 package.

**Running the Simulation**

ros2 run turtlesim turtlesim_node : Start the Turtlesim visualizer node.

ros2 run my_turtle_package move_turtle : Execute the pattern drawing node.

ros2 topic echo /turtle1/pose : Monitor the real-time position and orientation of the turtle.

ros2 service call /kill turtlesim/srv/Kill "{name: 'turtle1'}" : Remove the default turtle to clear the workspace.

# Problems Faced and Solutions

**Issue 1: Missing Subscriber Node (Turtlesim Window)**

Problem: I was running my custom Python node, and while the terminal showed data being published to /cmd_vel, no movement occurred because the Turtlesim window was not open.

Solution: Realized that for a publisher subscriber relationship to work, the turtlesim_node must be running to subscribe to the velocity commands.

**Issue 2: Wall Hitting and Path Drift**

Problem: When drawing larger shapes (Pentagon/Hexagon), the turtles initially hit the boundaries (0.0 or 11.0) or their paths shifted slightly every lap, creating a "messy" drawing.

Solution: Switched from time based movement to pose based feedback logic. I shunted the starting coordinates away from the walls and used the Euclidean distance formula to stop the turtle exactly when the side length was reached.

**Issue 3: Asynchronous Spawn Collisions**

Problem: Attempting to spawn three turtles and kill the default one simultaneously caused some turtles to fail to appear.

Solution: Implemented synchronous service calls using spin_until_future_complete to ensure each turtle was fully spawned before the next command was issued.

# Reflection

This lab bridged the gap between basic teleoperation and autonomous path planning. By implementing the point-to-point task, I learned how to use proportional control to adjust linear and angular velocity based on the error between the current pose and the target. Dealing with multiple turtles highlighted the importance of namespace management and coordinate frame awareness to prevent collisions in a shared environment. These skills are fundamental for moving from simple simulations to real world mobile robot navigation.
