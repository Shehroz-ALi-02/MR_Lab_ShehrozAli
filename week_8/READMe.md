# MCT-454L Mobile Robotics: Week 8 Lab
**Student Name: Shehroz Ali**

**Instructor: Dr. Maria Akram**

# Brief Description
This lab focused on constructing and configuring a custom Automated Guided Vehicle (AGV) / Autonomous Mobile Robot (AMR) using the Unified Robot Description Format (URDF) within a ROS 2 workspace. The primary objective was to move past theoretical architectures and transition into structural robot description modeling.I designed a multi-link differential-drive robot base equipped with balancing casters, a payload deck, and an elevated LiDAR sensor tower Using robot_state_publisher and tf2_tools, the robot's physical configuration, joints (fixed and continuous), and coordinate transformations (tf) were successfully compiled and visualized in real time inside RViz.

# Commands Used
**Workspace Setup & Package Installation**

sudo apt install ros-humble-urdf-tutorial: Install the official ROS 2 URDF visualization tutorial packages.

sudo apt install ros-humble-tf2-tools: Install the tf2 transformation utility tools

cd ~/ros2_ws/src/my_robot_description && mkdir urdf launch rviz: Navigate to the description package and create the required asset directory architecture

**Compilation, Execution & Visualization**

cd ~/ros2_ws: Navigate to the root of the ROS 2 workspace

colcon build: Compile the updated package structure and the custom URDF configuration.

source install/setup.bash: Source the updated overlay workspace into the current terminal shell.

ros2 launch urdf_tutorial display.launch.py model:=$(ros2 pkg prefix my_robot_description)/urdf/my_robot.urdf: Launch RViz alongside the joint state publisher GUI using the path of the custom robot model.

ros2 run tf2_tools view_frames: Execute the utility node to record and generate a visual PDF tree map of coordinate transforms between frames.

# Problems Faced and Solutions
**Issue 1: Joint-to-Link Parent/Child Naming Typos**

Problem: The example snippet code structure provided in the manual contained logic errors (e.g., mapping a fixed camera joint to a non-existent child link named "left wheel"), which caused the URDF parsing node to crash upon launch.

Solution: Debugged and rewrote the URDF file from scratch, ensuring explicit semantic agreement where every joint block accurately paired a valid parent link to an existing child link profile.

**Issue 2: Mechanical Misalignment & Ground Clearance Faults**

Problem: The robot model initially experienced physical instability. When aligning a spherical caster wheel to the same Z-axis joint offset as the larger side cylinders, the caster didn't align flat with the drive wheels on the ground plane, creating an uneven axis loop.

Solution: Applied precise coordinate geometry calculations. Set the drive wheels with a radius of 0.08m at an offset of -0.05m (ground touch at -0.13m) and matched it by choosing a caster radius of 0.04m at an offset of -0.09m (ground touch at -0.13m). Added a dual-caster assembly (front and rear) to completely eradicate structural tipping.

**Issue 3: Broken Transform (tf) Tree and Global Frame Errors in RViz**

Problem: When opening RViz, the robot geometry appeared completely white or invisible, generating a stream of "No transform from [base_link] to [map]" warning errors.

Solution: Realized that the default global fixed frame in RViz was unassigned.Configured a clean kinematic root link (base_footprint) fixed directly to the floor plane, and manually switched the RViz display Fixed Frame dropdown setting from map to base_footprint.

# Reflection
This lab marked a significant structural shift from manipulating pre-existing simulators to defining the physical architecture of a robot from the ground up Writing URDF descriptions taught me that a robot is essentially a tree of links connected by joints. Manually computing coordinate frame origins highlighted the absolute precision required to align transformations; a single math error can result in a robot that clips through floors or lacks balance. Inspecting the TF tree via view_frames helped bridge the gap between abstract XML descriptions and how ROS 2 handles multi-coordinate spatial orientation. This rigid spatial mapping forms the foundation for mapping physical sensor data (like LiDAR fields of view) accurately onto a moving chassis in upcoming physics simulations.
