import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, LaserScan
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge
import cv2
import numpy as np

class TrackingNode(Node):

    def __init__(self):
        super().__init__('tracking_node')

        # ---------------------------------------------
        # CAMERA SUBSCRIBER
        # ---------------------------------------------
        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )

        # ---------------------------------------------
        # LIDAR SUBSCRIBER
        # ---------------------------------------------
        self.lidar_sub = self.create_subscription(
            LaserScan,
            '/scan',  
            self.lidar_callback,
            10
        )

        # ---------------------------------------------
        # CMD VEL PUBLISHER
        # ---------------------------------------------
        self.cmd_pub = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        self.bridge = CvBridge()
        
        # --- PRESERVED TUNING PARAMETERS ---
        self.kp_angular = 0.4       
        self.max_angular_vel = 0.2  
        self.align_tolerance = 0.15 
        
        # --- NEW METRIC STOPPING DISTANCE ---
        self.current_distance = 999.0      # Fallback distance (meters)
        self.stop_distance_meters = 0.45   # Stops exactly 45 cm away from the box

        self.get_logger().info("Tracking Node Started - LiDAR Distance Stop Active")

    # =================================================
    # LIDAR CALLBACK
    # =================================================
    def lidar_callback(self, msg):
        if len(msg.ranges) > 0:
            # Index 0 is directly in front of the robot on standard LiDAR configurations
            front_distance = msg.ranges[0]
            
            # Filter out invalid or out-of-range readings
            if not np.isnan(front_distance) and not np.isinf(front_distance):
                self.current_distance = front_distance

    # =================================================
    # IMAGE CALLBACK
    # =================================================
    def image_callback(self, msg):
        try:
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        except Exception as e:
            self.get_logger().error(str(e))
            return

        # ---------------------------------------------
        # IMAGE INFO
        # ---------------------------------------------
        height, width, _ = frame.shape
        image_center_x = width / 2.0  

        # ---------------------------------------------
        # CONVERT TO HSV & MASK RED (UNTOUCHED)
        # ---------------------------------------------
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_red1 = np.array([0, 120, 70])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([170, 120, 70])
        upper_red2 = np.array([180, 255, 255])

        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask = mask1 + mask2

        # Clean up mask noise
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.erode(mask, kernel, iterations=1)
        mask = cv2.dilate(mask, kernel, iterations=2)

        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        twist = Twist()

        # =================================================
        # CONTROL LOGIC
        # =================================================
        if len(contours) > 0:
            largest_contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest_contour)

            if area > 400:
                x, y, w, h = cv2.boundingRect(largest_contour)
                cx = x + w // 2
                cy = y + h // 2

                # Calculate Normalized Error
                pixel_error = image_center_x - cx
                normalized_error = pixel_error / image_center_x

                self.get_logger().info(f"Dist: {self.current_distance:.2f}m | Norm Error: {normalized_error:.2f}", throttle_duration_sec=0.5)

                # Visual elements
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.circle(frame, (cx, cy), 6, (255, 0, 0), -1)
                cv2.line(frame, (int(image_center_x), 0), (int(image_center_x), height), (255, 255, 0), 2)

                # --- TARGET ALIGNMENT WINDOW ---
                if abs(normalized_error) < self.align_tolerance:
                    # Object is centered! Stop turning.
                    twist.angular.z = 0.0
                    
                    # CHANGED: Use LiDAR distance metric instead of pixel area to stop
                    if self.current_distance <= self.stop_distance_meters:
                        twist.linear.x = 0.0
                        status_txt = "TARGET REACHED"
                    else:
                        twist.linear.x = 0.08  # Drive forward straight
                        status_txt = "MOVING FORWARD"
                else:
                    # Object is out of tolerance -> Rotate on point until centered
                    twist.linear.x = 0.0
                    raw_turn = self.kp_angular * normalized_error
                    twist.angular.z = max(min(raw_turn, self.max_angular_vel), -self.max_angular_vel)
                    status_txt = "ALIGNING"

                cv2.putText(frame, status_txt, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            else:
                # UNTOUCHED: Small object logic
                twist.linear.x = 0.0
                twist.angular.z = 0.1
                cv2.putText(frame, "SMALL OBJECT", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        else:
            # UNTOUCHED: Search mode logic
            twist.linear.x = 0.0
            twist.angular.z = 0.12
            cv2.putText(frame, "SEARCHING", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Publish velocities and draw windows
        self.cmd_pub.publish(twist)
        cv2.imshow("Tracking", frame)
        cv2.imshow("Mask", mask)
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    node = TrackingNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down node...")
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
