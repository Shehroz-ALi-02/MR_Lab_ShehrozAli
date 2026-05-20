# MCT-454L Mobile Robotics: Week 9 Lab
**Student Name: Shehroz Ali**

**Instructor: Dr. Maria Akram**

# Brief Description
This lab focused on developing an adaptive, real-time reactive robotic controller by fusing 2D LiDAR telemetry and OpenCV camera vision within a ROS 2 network. Moving away from static sequential state machines, I developed a parallel opportunistic processing script that evaluates multiple sensor matrices concurrently. The robot is engineered to detect, distinguish, and respond uniquely to colored targets in its environment: it treats Blue objects as empty background space, uses Red targets as a critical one-way safety boundary, and dynamically tracks, centers, and approaches Green blocks using unified coordinate spatial alignment.

# Commands Used
**Workspace Setup & Package Execution**

cd ~/ros2_ws/src && ros2 pkg create --build-type ament_python my_tracking_node: Create a custom ROS 2 Python package skeleton inside the source workspace.

pip install opencv-python numpy: Ensure the local runtime environment has the required computer vision and numerical processing libraries installed.

colcon build --packages-select my_tracking_node: Compile only the updated tracking package to save development cycle time.

source install/setup.bash: Source the overlay workspace modifications into the active terminal shell interface.

**Node Execution & Diagnostic Monitoring**

ros2 run my_tracking_node tracking_executable: Launch the custom parallel tracking and sensor fusion node.

ros2 topic echo /cmd_vel: Stream the real-time velocity commands (`Twist` messages) being published by the controller.

ros2 topic hz /camera/image_raw: Verify that the camera feed publisher is maintaining its target frame rate for stable image callback processing.

# Problems Faced and Solutions
**Issue 1: Red Mask Flashing and Split-HSV Boundary Gaps**

*Problem:* Initial testing with simple HSV thresholding caused the Red target tracking mask to flash unstably under varying lighting conditions, occasionally dropping the target completely. This happened because the Red color profile naturally splits across the wrap-around boundary of the HSV space (0-10 deg and 170-180 deg).

*Solution:* Implemented a dual-masking parallel filter (`mask1 + mask2`) in the image processing block. By combining both segments and applying a 5x5 morphological kernel (one erosion pass followed by a dual dilation pass), high-frequency background noise was successfully filtered out, creating a stable visual tracking blob.

**Issue 2: Tractor-Beam Traps with Bidirectional Proportional Loops**

*Problem:* When trying to handle Red obstacles, the controller originally used a bidirectional proportional feedback loop to lock the robot at exactly 2.5 meters away. This created a logical deadlock: the robot became trapped in front of the Red block, unable to back up or drive away to find other targets.

*Solution:* Restructured the logic into a rigid, one-way safety boundary condition. If a Red target is detected further away than 2.5 meters, it is completely ignored, allowing the robot to continue spinning and hunting. The proactive reverse velocity command triggers *only* if the LiDAR data confirms that the target has breached the 2.5-meter limit.

**Issue 3: The Centroid-Halt Glitch (Premature Stopping on Green)**

*Problem:* The robot would stop prematurely the instant it caught a glimpse of the Green block's edge. This happened because a foreground LiDAR beam (hitting the floor or a wall) dipped below the distance threshold *before* the robot was actually facing the block.

*Solution:* Established a strict nested tracking priority. The node was rewritten to split the workflow into a two-step sequence: first, it forces a visual-only rotational loop to align the camera's center line with the block's physical centroid (`cx`). The controller completely ignores LiDAR range data during this turn. Only after centering is verified (Error_{normalized} < 0.15) does it activate the LiDAR braking range, driving straight forward to a clean 0.5-meter stop.

**Issue 4: High-Velocity Collisions and Tight-Radius Blindspots with Blue**

*Problem:* When attempting an orbital passing maneuver around the Blue blocks, the robot's forward momentum combined with its tight turning radius caused it to crash directly into the side of the obstacle.

*Solution:* Swapped the active tracking behavior with a complete exclusion strategy. Blue targets were removed entirely from the active sensor profiles, treating them as open, empty background space. This simplified the navigation landscape, ensuring the robot stayed focused on safety around Red and accuracy around Green.

# Reflection
This lab highlighted the difference between processing individual sensor feeds and building true, integrated sensor fusion. Working through the bugs taught me that combining vision data with LiDAR metrics requires carefully structured, nested priority rules rather than simple, global triggers. Forcing the robot to complete visual alignment before allowing the LiDAR to execute stopping routines proved essential for preventing false-positive braking bugs. Additionally, transitioning from a rigid sequential state machine to a parallel opportunistic collector showed that a truly adaptive robot must evaluate its entire sensor field at once. This logical architecture provides the flexible, real-time decision-making foundation needed for real-world autonomous navigation in unpredictable environments.
