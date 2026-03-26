import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time

class TriangleMover(Node):

    def __init__(self):
        super().__init__('triangle_mover')
        self.publisher_ = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)
        self.step = 0
        self.timer = self.create_timer(0.1, self.timer_callback)

    def timer_callback(self):
        msg = Twist()

        if self.step == 0:
            # Move forward
            msg.linear.x = 2.0
            msg.angular.z = 0.0
            self.publisher_.publish(msg)
            time.sleep(2)
            self.step += 1
        elif self.step == 1:
            # Turn 120 degrees
            msg.linear.x = 0.0
            msg.angular.z = 2.094
            self.publisher_.publish(msg)
            time.sleep(1)
            self.step += 1
        elif self.step == 2:
            msg.linear.x = 2.0
            msg.angular.z = 0.0
            self.publisher_.publish(msg)
            time.sleep(2)
            self.step += 1
        elif self.step == 3:
            msg.linear.x = 0.0
            msg.angular.z = 2.094
            self.publisher_.publish(msg)
            time.sleep(1)
            self.step += 1
        elif self.step == 4:
            msg.linear.x = 2.0
            msg.angular.z = 0.0
            self.publisher_.publish(msg)
            time.sleep(2)
            self.step += 1
        elif self.step == 5:
            msg.linear.x = 0.0
            msg.angular.z = 2.094
            self.publisher_.publish(msg)
            time.sleep(1)
            self.step = 0  # Reset to repeat triangle

def main(args=None):
    rclpy.init(args=args)
    node = TriangleMover()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
