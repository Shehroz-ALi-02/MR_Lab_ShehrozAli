# *Week_1: Post Lab Question's Answers.*
## 1. Define: node, topic, package, workspace. Provide one sentence each. 
**Node**: A Ros node is an exectuable process with in the robot operating system framework that performs a specific computation or fine grade task within the ROS 2 graph (e.g., a sensor driver or a controller). Nodes uses ROS client libraries to exchange data through topics acting as a fundamental building block of the ROS architecture.
**Topic**: A named bus/channel used by the node to exchange messages using a publisher subscriber model enabling decoupled, asynchronous and many to many communication for data streams like sensor data. Node Publish data to the topic and subscribe to recieve the data typically via TCP/IP. Data flow in one direction from publisher to subscriber and mutiple nodes can publish or subscribe to same topic simutaneously.
**Package**: A container that contain nodes, libraries, datasets, configurations files etc. Packages allow for the modeular development, building, and  sharing of functionality ensuring code is portable, reusable and executable. They are typically created within src directory in workspace making it easy to share and build software.
**Workspace**: A main folder like (ShehrozAli_ws) on your computer where you develop, build, and install ROS packages. It contain src folder for source code and build, log and install. Use differnet workspaces for different projects to avoid dependecncy conflicts. 

# 2. Explain why sourcing is required. What happens if you do not source a workspace?
Sourcing is the process of loading/updating enviromental variables (like PATH and PYTHONPATH) so the system is aware where ROS and your built packages are located. If you do not source the workspace, it ill make the system blind from your project and commands like ros run will fail with a "Package not found" error.

# 3. What is the purpose of colcon build? What folders does it generate?
colcon build is the command line tool used to build, test, install, compile the multiple software packages or  source code in your workspace that is automating the process and managing dependecies. It is the standard tool for ROS and generates three main folders build, install and log when run in the workspace that contain src as a peer of src folder.

# 4. In your own words, explain what the entry_points console script does in setup.py.
The entry points is the console script in setup.py serves as a mechanism to automatically create executable command line tools when your Python package is installed. It essentially maps a command line name to a specific Python function within your package.

# 5. Draw (by hand or ASCII) a diagram showing one publisher and one subscriber connected by a topic.
            Node A   --- (Topic: /cmd_vel) --->     Node B 
          (Publisher)                             (Subscriber)


