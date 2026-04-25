import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class VelocityPublisher(Node):
    def __init__(self):
        super().__init__('velocity_publisher')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.timer = self.create_timer(2.0, self.timer_callback)
        self.is_moving = False

    def timer_callback(self):
        msg = Twist()
        if not self.is_moving:
            msg.linear.x = 0.15  # Move forward at 0.15 m/s
            self.get_logger().info('Status: MOVING FORWARD')
        else:
            msg.linear.x = 0.0   # Stop
            self.get_logger().info('Status: STOPPED')

        self.publisher_.publish(msg)
        self.is_moving = not self.is_moving

def main(args=None):
    rclpy.init(args=args)
    node = VelocityPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()
