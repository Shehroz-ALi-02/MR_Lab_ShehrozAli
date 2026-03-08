MCT-454L Mobile Robotics: Week 1 Lab                                
Student Name: Shehroz Ali
Instructor: Dr. Maria Akram

Brief Description
This lab served as an onboarding session for Linux and ROS 2 Humble. The primary objectives were to familiarize ourselves with terminal navigation, set up a standard ROS 2 development workspace (ros2_ws), and create a Python based package. I successfully implemented a basic node that utilizes the ROS 2 logging system and registered it as an executable through the package build system.

Commands Used:
The following key commands were utilized during the lab session:
# Linux Navigation
pwd && ls -l
mkdir -p ~/ros2_ws/src

# ROS 2 Environment & Build
source /opt/ros/humble/setup.bash
cd ~/ros2_ws
colcon build

# Package & Node Management
cd src
ros2 pkg create --build-type ament_python my_first_pkg
source ../install/setup.bash
ros2 run my_first_pkg simple_node


Problems Faced and Solutions
Issue 1: Environment Not Found
Problem: Running ros2 commands resulted in "command not found."
Solution: I sourced the global ROS 2 setup file using source /opt/ros/humble/setup.bash and later automated this by adding it to my .bashrc.

Issue 2: Executable Recognition
Problem: ros2 run could not locate simple_node even after the file was created.
Solution: I verified the console_scripts entry in setup.py, ensured the Python script had executable permissions (chmod +x), and performed a fresh colcon build.

Issue 3: Path and Workspace Naming Errors
Problem: Initially, copy-pasting commands from the manual caused errors because the default workspace names in the commands did not match my actual folder structure.
Solution: I identified that I needed to customize the workspace paths in my terminal commands and within setup.py to match my specific directory name rather than blindly following the generic manual examples.

Issue 4: Version Check Command Error
Problem: The command ros --version (or ros2 --version in some environments) resulted in "command not found" or did not provide the distribution information.
Solution: I used the correct ROS 2 command ros2 --version or checked the installed distribution using printenv | grep ROS_DISTRO to confirm I was using Humble.

Reflection:
This introductory lab provided a crucial foundation for working with distributed robotic systems. Transitioning from a standard programming environment to the ROS 2 ecosystem highlighted the importance of workspace management and the "build-source-run" cycle. Learning how ROS 2 abstracts complex communication into nodes and topics makes it clear why this framework is industry-standard for scalable robotics. I found the process of registering entry points in setup.py to be a vital link between writing raw Python code and creating a deployable ROS component.
One of the most valuable lessons was troubleshooting environment variables and path structures. I realized that while manuals provide a great template, I must be attentive to my specific workspace naming conventions to avoid directory errors. This experience taught me that precision in the Linux terminal and an understanding of file paths are just as important as the code itself. The modular structure of the ament_python build type is impressive, as it organizes dependencies and metadata in a way that simplifies collaboration. I am looking forward to moving beyond basic logging to implement actual publisher-subscriber logic in the coming weeks. Overall, this lab successfully bridged the gap between theoretical concepts and practical development environment setup.
