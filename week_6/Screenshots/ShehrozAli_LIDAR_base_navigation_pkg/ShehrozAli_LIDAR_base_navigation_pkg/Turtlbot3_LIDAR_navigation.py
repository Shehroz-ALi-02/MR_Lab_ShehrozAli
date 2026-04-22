import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import numpy as np

class LidarNavigator(Node):
    def __init__(self):
        super().__init__('Turtlbot3_LIDAR_navigation')
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10)
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # Optimized thresholds for pillars and walls
        self.front_threshold = 0.3  # Start reacting earlier
        self.side_threshold = 0.25   # Keep distance from side walls
        
    def scan_callback(self, msg):
        ranges = np.array(msg.ranges)
        
        # Clean data: Replace invalid readings with max range
        ranges[np.isinf(ranges)] = msg.range_max
        ranges[np.isnan(ranges)] = msg.range_max

        # Define regions (30 degrees for front to capture thin pillars)
        front_indices = np.concatenate((ranges[0:20], ranges[340:360]))
        left_indices = ranges[20:100]
        right_indices = ranges[260:340]

        # Compute minimum distance in each sector
        front_dist = np.min(front_indices)
        left_dist = np.min(left_indices)
        right_dist = np.min(right_indices)

        twist = Twist()

        # Logic for Pillars and Boundaries
        if front_dist < self.front_threshold:
            # Obstacle detected! 
            # We use a tiny bit of linear speed (0.02) to help pivot 
            # smoothly rather than spinning in place like a top.
            twist.linear.x = 0.02 
            
            if left_dist > right_dist:
                self.get_logger().info('Object Front: Turning Left')
                twist.angular.z = 0.5
            else:
                self.get_logger().info('Object Front: Turning Right')
                twist.angular.z = -0.5
        else:
            # Path is clear - Move forward
            twist.linear.x = 0.15  # Good cruising speed
            
            # Subtle "Nudge" logic: stay away from side pillars while moving
            if left_dist < self.side_threshold:
                twist.angular.z = -0.2  # Nudge right
            elif right_dist < self.side_threshold:
                twist.angular.z = 0.2   # Nudge left
            else:
                twist.angular.z = 0.0   # Go straight

        self.publisher.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = LidarNavigator()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Keyboard Interrupt (Ctrl+C) detected.')
    finally:
        # Emergency Stop: Publish a zero velocity message before exiting
        stop_msg = Twist()
        stop_msg.linear.x = 0.0
        stop_msg.angular.z = 0.0
        node.publisher.publish(stop_msg)
        
        node.get_logger().info('Robot Stopped. Shutting down node.')
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
