from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess

def generate_launch_description():
    return LaunchDescription([
        # Starts the simulator window
        Node(package='turtlesim', executable='turtlesim_node', name='sim'),
        
        # Spawns the second turtle via service call
        ExecuteProcess(
            cmd=[['ros2 service call /spawn turtlesim/srv/Spawn "{x: 2.0, y: 2.0, name: \'turtle2\'}"']],
            shell=True
        ),

        # Launches the Python "Brain" we just wrote
        Node(package='ShehrozAli_launch_pkg', executable='follower_node', name='follower_logic'),

        # Opens the control window for the first turtle
        Node(package='turtlesim', executable='turtle_teleop_key', prefix='xterm -e')
    ])
