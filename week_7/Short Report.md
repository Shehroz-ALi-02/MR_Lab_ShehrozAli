# Deliverable 1: Short Report of Steps and Observations
## 1. Simulation & Setup

    Step: Launched the TurtleBot3 world in Gazebo and the Nav2 stack with the pre-saved map from Lab 5.

    Observation: The Map Server successfully loaded my_map.yaml, and the static environment appeared in RViz.

## 2. Localization (AMCL)

    Step: Used the 2D Pose Estimate tool in RViz to set the initial pose and used teleoperation to move the robot slightly.

    Observation: The initial red particle cloud was scattered but quickly converged around the robot as the LiDAR scans matched the map walls. This confirmed the AMCL particle filter was working.

## 3. Navigation & Waypoints

    Step: Sent single goals via RViz and then executed a 5-waypoint mission using a custom Python node (waypoint_navigator.py).

    Observation: The planner_server generated a smooth global path (green line), and the controller_server maintained the robot's velocity to follow the path accurately.

# Deliverable 6: Written Observations on Recovery Behavior (Task 5)

Scenario: A dynamic obstacle (box) was placed in the robot's path while it was moving toward a waypoint.

Observations:

    Detection: The Local Costmap immediately showed a new lethal obstacle (purple/red zone) that was not part of the original static map.

    Action: The robot initially paused. When it realized the path was completely blocked, the recoveries_server triggered a Spin behavior.

    Resolution: After spinning to "clear" its local costmap and find an opening, the bt_navigator requested a new plan. The robot successfully re-planned a trajectory around the box and continued to its   destination.

# Deliverable 7: Conclusion
This lab provided a comprehensive look at the ROS 2 Navigation (Nav2) ecosystem. I learned how to integrate individual components—Map Server, AMCL Localization, and the Waypoint Follower into a functional autonomous system.

## Challenges Faced

    Initial Pose: If the initial 2D Pose Estimate was off by more than 0.5 meters, the robot would plan paths through walls.

    Costmap Tuning: Understanding that the local costmap is a rolling window that moves with the robot was essential for debugging obstacle avoidance.

## SLAM (Lab 5) vs. Navigation (Lab 7)

The workflow difference is significant:

    SLAM is an exploratory process where the robot discovers the environment and builds a coordinate system from scratch.

    Navigation is a "knowledge-based" process. The robot uses a fixed reference (the map) to solve the "Where am I?" problem (Localization) and the "How do I get there?" problem (Path Planning). While SLAM focuses on discovery, Navigation focuses on precision and reliability.
