from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess

def generate_launch_description():
    return LaunchDescription([
        # 1. The Single Simulator Window
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='sim',
            output='screen'
        ),

        # 2. Spawn a second turtle (turtle2) at x=3.0, y=3.0
        ExecuteProcess(
            cmd=[[
                'ros2 service call /spawn turtlesim/srv/Spawn "{x: 3.0, y: 3.0, theta: 0.0, name: \'turtle2\'}"'
            ]],
            shell=True
        ),

        # 3. Teleop for the first turtle (default turtle1)
        Node(
            package='turtlesim',
            executable='turtle_teleop_key',
            name='teleop_turtle1',
            prefix='xterm -e',
            output='screen',
            remappings=[('/turtle1/cmd_vel', '/turtle1/cmd_vel')] # Standard
        ),

        # 4. Teleop for the second turtle (remapped to turtle2)
        Node(
            package='turtlesim',
            executable='turtle_teleop_key',
            name='teleop_turtle2',
            prefix='xterm -e',
            output='screen',
            remappings=[('/turtle1/cmd_vel', '/turtle2/cmd_vel')] # Crucial Remap
        )
    ])
