import rclpy
from rclpy.node import Node 
from geometry_msgs.msg import Twist 

class CircleMover(Node): 
    def __init__(self): 
        # Initialize the node with the name 'circle_mover'
        super().__init__('circle_mover') 
        
        # Create a publisher to the 'turtle1/cmd_vel' topic
        self.publisher_ = self.create_publisher(Twist, 'turtle1/cmd_vel', 10) 
        
        # Create a timer that calls the callback every 0.1 seconds (10Hz)
        self.timer = self.create_timer(0.1, self.timer_callback) 

    def timer_callback(self): 
        msg = Twist() 
        msg.linear.x = 2.0  # Constant forward velocity
        msg.angular.z = 1.0 # Constant rotation speed
        self.publisher_.publish(msg) 

def main(args=None): 
    rclpy.init(args=args) 
    node = CircleMover() 
    
    try:
        rclpy.spin(node) 
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node() 
        rclpy.shutdown() 

if __name__ == '__main__': 
    main()
