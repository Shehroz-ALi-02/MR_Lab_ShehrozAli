import rclpy
from rclpy.node import Node
import os

counter_file = os.path.join(os.path.dirname(__file__), "run_count.txt")

class SimpleNode(Node):
    def __init__(self):
        super().__init__('simple_node')
        self.get_logger().info('Hello, ROS2 \n Welcome to Mobile Robotics Lab')
        self.update_run_count()

    def update_run_count(self):
        if os.path.exists(counter_file):
            with open(counter_file, "r") as f:
                data = f.read().strip()
                count = int(data) if data else 0
        else:
            count = 0

        count += 1

        with open(counter_file, "w") as f:
            f.write(str(count))

        self.get_logger().info(f"Node run count updated to: {count}")

def main(args=None):
    rclpy.init(args=args)
    node = SimpleNode()
    rclpy.spin_once(node, timeout_sec=0.1)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
