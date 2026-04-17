import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import math

class TurtleFollower(Node):
    def __init__(self):
        super().__init__('turtle_follower')
        
        # Subscriber to Turtle 1's position
        self.pose_sub = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        
        # Subscriber to Turtle 2's position (so it knows where IT is)
        self.self_pose_sub = self.create_subscription(Pose, '/turtle2/pose', self.own_pose_callback, 10)
        
        # Publisher for Turtle 2's movement
        self.cmd_pub = self.create_publisher(Twist, '/turtle2/cmd_vel', 10)
        
        self.target_pose = None
        self.current_pose = None

    def pose_callback(self, msg):
        self.target_pose = msg
        self.move_follower()

    def own_pose_callback(self, msg):
        self.current_pose = msg

    def move_follower(self):
        if self.target_pose is None or self.current_pose is None:
            return

        msg = Twist()
        
        # Calculate distance between turtles
        dist = math.sqrt(
            (self.target_pose.x - self.current_pose.x)**2 + 
            (self.target_pose.y - self.current_pose.y)**2
        )

        # Calculate angle to the leader
        angle_to_target = math.atan2(
            self.target_pose.y - self.current_pose.y,
            self.target_pose.x - self.current_pose.x
        )
        
        # 1. Proportional Control for Linear Velocity
        # If distance > 1.0, move. If very close, stop.
        if dist > 1.0:
            msg.linear.x = 2 * dist
            
            # 2. Proportional Control for Angular Velocity
            # Subtract current heading from target angle
            angle_diff = angle_to_target - self.current_pose.theta
            
            # Normalize angle to stay between -pi and pi
            if angle_diff > math.pi: angle_diff -= 2*math.pi
            if angle_diff < -math.pi: angle_diff += 2*math.pi
           
            msg.angular.z = 10 * angle_diff
        else:
            msg.linear.x = 0.0
            msg.angular.z = 0.0

        self.cmd_pub.publish(msg)

def main():
    rclpy.init()
    node = TurtleFollower()
    rclpy.spin(node)
    rclpy.shutdown()
