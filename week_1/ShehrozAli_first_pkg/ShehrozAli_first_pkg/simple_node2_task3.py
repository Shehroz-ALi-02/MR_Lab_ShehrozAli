# simple_node2.py
import rclpy
from rclpy.node import Node
import os

# Path to the counter file
counter_file = os.path.join(os.path.dirname(__file__), "run_count.txt")

class CounterNode(Node):
    def __init__(self):
        super().__init__('counter_node')
        self.show_run_count()

    def show_run_count(self):
        if os.path.exists(counter_file):
            with open(counter_file, "r") as f:
                count = int(f.read().strip())
        else:
            count = 0
        self.get_logger().info(f"Node 1 has been run {count} times")

def main(args=None):
    rclpy.init(args=args)
    node = CounterNode()
    rclpy.spin_once(node, timeout_sec=0.1)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
