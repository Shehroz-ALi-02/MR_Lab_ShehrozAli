import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import threading

class LoopingTurtleMover(Node):
    def __init__(self):
        super().__init__('looping_turtle_mover')
        
        self.target_x = None
        self.target_y = None
        self.tolerance = 0.1
        
        self.publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.subscription = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        
        self.pose = Pose()
        self.timer = self.create_timer(0.02, self.control_loop)
        
        # Start a background thread to handle user input
        self.input_thread = threading.Thread(target=self.ask_user_input)
        self.input_thread.daemon = True
        self.input_thread.start()

    def pose_callback(self, msg):
        self.pose = msg

    def ask_user_input(self):
        """ This runs in a separate thread so it doesn't block the turtle's movement """
        while rclpy.ok():
            try:
                print("\n--- Standing by for new Goal ---")
                tx = float(input("Enter Target X (0.0 - 11.0): "))
                ty = float(input("Enter Target Y (0.0 - 11.0): "))
                
                # Update the targets
                self.target_x = tx
                self.target_y = ty
                self.get_logger().info(f"New Target Set: ({tx}, {ty})")
                
                # Wait until the turtle reaches the goal before asking again
                while self.target_x is not None and rclpy.ok():
                    import time
                    time.sleep(0.5)
                    
            except ValueError:
                print("Invalid input! Use numbers only.")

    def control_loop(self):
        # Do nothing if no target is set
        if self.target_x is None or self.pose.x == 0.0:
            return

        msg = Twist()
        dist = math.sqrt((self.target_x - self.pose.x)**2 + (self.target_y - self.pose.y)**2)
        
        if dist > self.tolerance:
            goal_theta = math.atan2(self.target_y - self.pose.y, self.target_x - self.pose.x)
            angle_error = math.atan2(math.sin(goal_theta - self.pose.theta), 
                                     math.cos(goal_theta - self.pose.theta))

            if abs(angle_error) > 0.05:
                msg.linear.x = 0.0
                msg.angular.z = 2.0 * angle_error
            else:
                msg.linear.x = 1.5 * dist
                msg.angular.z = 0.0
        else:
            # Goal reached: stop moving and clear target to allow next input
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.get_logger().info("Goal Reached! Ready for next location.")
            self.target_x = None
            self.target_y = None

        self.publisher.publish(msg)

def main():
    rclpy.init()
    node = LoopingTurtleMover()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
