## Observations
**Robot Behavior Near Obstacles**

The robot demonstrated reliable Reactive Navigation by utilizing a "See-Act" loop. When the front distance dropped below the 0.5m threshold, the robot successfully halted its linear progression. The decision making logic turning toward the side with the maximum clearance allowed it to navigate through the turtlebot3_world without manual intervention.

**Oscillations and Instability**

Corner "Jitter" Minor oscillations were observed when the robot entered narrow corners. Because the LiDAR data fluctuates slightly, the robot would rapidly switch between "Turn Left" and "Turn Right" commands. This instability was partially mitigated by using a minimum filter over a range of degrees rather than relying on a single LiDAR beam index.

**Effect of Threshold Values** 

High Threshold 0.8m so the robot became overly "cautious," often triggering avoidance maneuvers in wide-open spaces or getting stuck in large corridors because it perceived distant walls as immediate threats.Low Threshold is 0.3m so the robot frequently collided with obstacles. Due to the robot’s inertia, the stopping distance was insufficient to prevent physical contact after the command was issued.A threshold of 0.5m provided the best balance between safety and fluid movement.

## Conclusion
This lab successfully demonstrated the implementation of Reactive Navigation using ROS 2 and LiDAR data. The core learning outcome was the transformation of raw /scan arrays into actionable motion commands (/cmd_vel).Key Takeaways are:

1. Data Processing: Slicing the 360 degree LiDAR data into functional regions (front, left, right) is essential for directional awareness.

2. Control Logic: While simple if-else logic works for basic obstacle avoidance, more complex behaviors like wall following require proportional control to prevent jerky movements.

3. Challenges: The primary challenge faced was handling "noisy" sensor data and inf values. Learning to clean this data using numpy was critical for preventing the node from crashing or making erratic turns. In summary, the robot proved capable of navigating a simulated environment without a pre existing map, laying the groundwork for more advanced autonomous path planning tasks.
