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
        # SUBSCRIBER & PUBLISHER SETUP
        # ---------------------------------------------
        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )

        self.lidar_sub = self.create_subscription(
            LaserScan,
            '/scan',  
            self.lidar_callback,
            10
        )

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
        
        # --- SPEED AND BRAKING LIMITS ---
        self.forward_speed = 0.25         # Snappy cruise speed (m/s)
        self.stop_distance_meters = 2     # Stop roughly 85cm away
        
        # --- SENSOR FUSION MINIMUM AREA ---
        # The target block must be majorly visible in the frame to trigger a stop.
        # This completely stops background noise from triggering changes.
        self.min_stop_area = 350000        

        # --- STATE MACHINE CONTROL ---
        self.current_target = 'RED' 
        self.current_distance = 999.0      

        self.get_logger().info("Tracking Node Started - Bulletproof Fusion Active")

    # =================================================
    # LIDAR CALLBACK
    # =================================================
    def lidar_callback(self, msg):
        if len(msg.ranges) > 0:
            # Look at absolute index 0 (straight ahead)
            front_distance = msg.ranges[0]
            if not np.isnan(front_distance) and not np.isinf(front_distance) and front_distance > 0.0:
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

        height, width, _ = frame.shape
        image_center_x = width / 2.0  
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Finished State Halt
        if self.current_target == 'FINISHED':
            twist = Twist()
            self.cmd_pub.publish(twist)
            cv2.putText(frame, "ALL TARGETS COMPLETED!", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 0), 2)
            cv2.imshow("Tracking", frame)
            cv2.waitKey(1)
            return

        # =================================================
        # DYNAMIC COLOR MASKING SELECTOR
        # =================================================
        if self.current_target == 'RED':
            lower_red1 = np.array([0, 120, 70])
            upper_red1 = np.array([10, 255, 255])
            lower_red2 = np.array([170, 120, 70])
            upper_red2 = np.array([180, 255, 255])
            mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
            mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
            mask = mask1 + mask2
            text_color = (0, 0, 255)

        elif self.current_target == 'GREEN':
            lower_green = np.array([35, 60, 60])
            upper_green = np.array([85, 255, 255])
            mask = cv2.inRange(hsv, lower_green, upper_green)
            text_color = (0, 255, 0)

        elif self.current_target == 'BLUE':
            lower_blue = np.array([100, 60, 60])
            upper_blue = np.array([140, 255, 255])
            mask = cv2.inRange(hsv, lower_blue, upper_blue)
            text_color = (255, 0, 0)

        # Clean mask noise
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.erode(mask, kernel, iterations=1)
        mask = cv2.dilate(mask, kernel, iterations=2)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        twist = Twist()

        # =================================================
        # CONTROL STATE LOGIC
        # =================================================
        if len(contours) > 0:
            largest_contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest_contour)

            # Filter valid objects from tiny background specs
            if area > 600:
                x, y, w, h = cv2.boundingRect(largest_contour)
                cx = x + w // 2
                cy = y + h // 2

                pixel_error = image_center_x - cx
                normalized_error = pixel_error / image_center_x

                self.get_logger().info(f"Target: {self.current_target} | Dist: {self.current_distance:.2f}m | Area: {area:.0f}", throttle_duration_sec=0.5)

                # UI Graphics
                cv2.rectangle(frame, (x, y), (x + w, y + h), text_color, 2)
                cv2.circle(frame, (cx, cy), 6, (255, 255, 255), -1)
                cv2.line(frame, (int(image_center_x), 0), (int(image_center_x), height), (255, 255, 0), 2)

                # --- STEP 1: ALIGNMENT CHECK ---
                if abs(normalized_error) < self.align_tolerance:
                    # Target is locked in the center line
                    twist.angular.z = 0.0
                    
                    # --- STEP 2: METRIC & VISUAL FUSION STOP CHECK ---
                    # It will ONLY trigger a target change if BOTH conditions are met simultaneously:
                    # 1. The LiDAR confirms something is close ahead (< 0.85m)
                    # 2. The targeted color block fills up a huge part of the screen (> 50,000 pixels)
                    if self.current_distance <= self.stop_distance_meters and area >= self.min_stop_area:
                        twist.linear.x = 0.0
                        
                        if self.current_target == 'RED':
                            self.get_logger().warn(">>> RED TARGET REACHED! SWITCHING TO GREEN <<<")
                            self.current_target = 'GREEN'
                        elif self.current_target == 'GREEN':
                            self.get_logger().warn(">>> GREEN TARGET REACHED! SWITCHING TO BLUE <<<")
                            self.current_target = 'BLUE'
                        elif self.current_target == 'BLUE':
                            self.get_logger().warn(">>> ALL TARGETS REACHED! FINISHING RUN <<<")
                            self.current_target = 'FINISHED'
                        
                        status_txt = "TARGET CHANGED"
                    else:
                        # Target is centered but far away -> Drive forward safely
                        twist.linear.x = self.forward_speed  
                        status_txt = f"APPROACHING {self.current_target}"
                else:
                    # Target is off-center -> Rotate on point to center it
                    twist.linear.x = 0.0
                    raw_turn = self.kp_angular * normalized_error
                    twist.angular.z = max(min(raw_turn, self.max_angular_vel), -self.max_angular_vel)
                    status_txt = f"ALIGNING {self.current_target}"

                cv2.putText(frame, status_txt, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, text_color, 2)
            else:
                # Bounding contour is a tiny background speck -> Treat as blind search spin
                twist.linear.x = 0.0
                twist.angular.z = 0.16
                cv2.putText(frame, f"SEARCHING FOR {self.current_target}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 165, 255), 2)
        else:
            # Target color completely missing from camera sight -> Spin in place to search
            twist.linear.x = 0.0
            twist.angular.z = 0.16 
            cv2.putText(frame, f"SEARCHING FOR {self.current_target}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 165, 255), 2)

        # Publish velocity commands and open UI frames
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
