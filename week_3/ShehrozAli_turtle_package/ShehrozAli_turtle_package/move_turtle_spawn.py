import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import Spawn, Kill
import math

class MultiTurtleStabilized(Node):
    def __init__(self):
        super().__init__('multi_turtle_stabilized')
        
        self.lin_speed = 2.0
        self.ang_speed = 1.5

        # SAFE SETTINGS: Reduced lengths slightly to guarantee no wall hits
        # Penta (Left), Hexa (Right), Rect (Top)
        self.turtles_info = {
            'penta': {'sides': 5, 'len': 1.8, 'x': 2.0, 'y': 2.0},
            'hexa':  {'sides': 6, 'len': 1.6, 'x': 8.5, 'y': 2.5},
            'rect':  {'sides': 4, 'len': 3.0, 'width': 1.5, 'x': 3.5, 'y': 8.0},
        }

        self.turtle_data = {}
        self.setup_world()
        self.timer = self.create_timer(0.02, self.control_loop)

    def setup_world(self):
        kill_client = self.create_client(Kill, 'kill')
        spawn_client = self.create_client(Spawn, 'spawn')

        while not kill_client.wait_for_service(1.0) or not spawn_client.wait_for_service(1.0):
            self.get_logger().info('Waiting for services...')

        # Remove default turtle
        kill_future = kill_client.call_async(Kill.Request(name='turtle1'))
        rclpy.spin_until_future_complete(self, kill_future)

        # Spawn custom turtles
        for name, info in self.turtles_info.items():
            req = Spawn.Request(x=info['x'], y=info['y'], theta=0.0, name=name)
            spawn_future = spawn_client.call_async(req)
            rclpy.spin_until_future_complete(self, spawn_future)

            self.turtle_data[name] = {
                'pose': Pose(),
                'state': 'MOVE',
                'start_pos': (info['x'], info['y']),
                'target_angle': 0.0,
                'side_index': 0,
                'pub': self.create_publisher(Twist, f'/{name}/cmd_vel', 10)
            }
            
            # Use default argument in lambda to fix scope issues
            self.create_subscription(Pose, f'/{name}/pose', 
                lambda msg, n=name: self.update_pose(msg, n), 10)

    def update_pose(self, msg, name):
        if name in self.turtle_data:
            self.turtle_data[name]['pose'] = msg

    def control_loop(self):
        for name, info in self.turtles_info.items():
            data = self.turtle_data[name]
            curr = data['pose']
            
            # Wait for valid pose data
            if curr.x == 0.0 and curr.y == 0.0:
                continue

            twist = Twist()

            # Handle side length for Rectangle vs Polygons
            if name == 'rect':
                current_side_len = info['len'] if data['side_index'] % 2 == 0 else info['width']
            else:
                current_side_len = info['len']

            if data['state'] == 'MOVE':
                # Calculate Euclidean distance
                dist = math.sqrt((curr.x - data['start_pos'][0])**2 + (curr.y - data['start_pos'][1])**2)
                
                if dist < current_side_len:
                    twist.linear.x = self.lin_speed
                else:
                    twist.linear.x = 0.0
                    data['state'] = 'TURN'
                    # Determine turn angle
                    angle_inc = (math.pi / 2) if name == 'rect' else (2 * math.pi / info['sides'])
                    goal = curr.theta + angle_inc
                    # Normalize to [-pi, pi]
                    data['target_angle'] = math.atan2(math.sin(goal), math.cos(goal))

            elif data['state'] == 'TURN':
                # Shortest path angle error
                err = math.atan2(math.sin(data['target_angle'] - curr.theta), 
                                 math.cos(data['target_angle'] - curr.theta))

                if abs(err) > 0.02:
                    twist.angular.z = self.ang_speed if err > 0 else -self.ang_speed
                else:
                    twist.angular.z = 0.0
                    data['state'] = 'MOVE'
                    data['start_pos'] = (curr.x, curr.y)
                    data['side_index'] += 1
            
            data['pub'].publish(twist)

def main():
    rclpy.init()
    node = MultiTurtleStabilized()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
