import rclpy
from rclpy.node import Node

class StudentNode(Node):

    def __init__(self):
        super().__init__('student_node')

        # Declare parameter
        self.declare_parameter('student_name', '')

        name = self.get_parameter('student_name').value

        if name:
            self.get_logger().info(f"Student name: {name}")
        else:
            self.get_logger().info("student_name not set")


def main(args=None):
    rclpy.init(args=args)

    node = StudentNode()

    rclpy.spin_once(node, timeout_sec=1)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
