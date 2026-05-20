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
        
        # --- SPEED LIMITS ---
        self.forward_speed = 0.25         # Snappy cruise speed (m/s)
        
        # --- TARGET CONSTRAINTS (UPDATED) ---
        self.red_safety_dist = 2.5        # Keep out boundary: Back up if closer than 2.5m
        self.green_stop_dist = 0.5        # Pure LiDAR stop threshold at 0.5m

        # --- LIVE DATA SENSOR STATE ---
        self.current_distance = 999.0      

        # --- HSV COLOR DEFINITIONS (BLUE EXCLUDED) ---
        self.color_profiles = {
            'RED': {
                'text_color': (0, 0, 255),
                'bounds': [
                    (np.array([0, 120, 70]), np.array([10, 255, 255])),
                    (np.array([170, 120, 70]), np.array([180, 255, 255]))
                ]
            },
            'GREEN': {
                'text_color': (0, 255, 0),
                'bounds': [(np.array([35, 60, 60]), np.array([85, 255, 255]))]
            }
        }

        self.get_logger().info("Tracking Node Started - Centered Green Approach @ 0.5m Active")

    def lidar_callback(self, msg):
        if len(msg.ranges) > 0:
            front_distance = msg.ranges[0]
            if not np.isnan(front_distance) and not np.isinf(front_distance) and front_distance > 0.0:
                self.current_distance = front_distance

    def image_callback(self, msg):
        try:
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        except Exception as e:
            self.get_logger().error(str(e))
            return

        height, width, _ = frame.shape
        image_center_x = width / 2.0  
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        kernel = np.ones((5, 5), np.uint8)

        red_target = None
        green_target = None

        # Process Red and Green masks in parallel
        for color_name, profile in self.color_profiles.items():
            color_mask = None
            for lower, upper in profile['bounds']:
                m = cv2.inRange(hsv, lower, upper)
                color_mask = m if color_mask is None else color_mask + m
            
            color_mask = cv2.erode(color_mask, kernel, iterations=1)
            color_mask = cv2.dilate(color_mask, kernel, iterations=2)
            
            contours, _ = cv2.findContours(color_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if len(contours) > 0:
                largest_contour = max(contours, key=cv2.contourArea)
                area = cv2.contourArea(largest_contour)
                
                if area > 600:  
                    x, y, w, h = cv2.boundingRect(largest_contour)
                    target_data = {
                        'area': area,
                        'cx': x + w // 2,
                        'cy': y + h // 2,
                        'box': (x, y, w, h),
                        'text_color': profile['text_color']
                    }
                    if color_name == 'RED':
                        red_target = target_data
                    elif color_name == 'GREEN':
                        green_target = target_data

        twist = Twist()
        status_txt = "SCANNING ENVIRONMENT..."

        # =================================================
        # PRIORITY EXECUTION MATRIX
        # =================================================
        
        # --- CONDITION 1: RED CRITICAL SAFETY INTERVENTION ---
        # Triggers ONLY if Red is seen AND breached the 2.5m limit
        if red_target is not None and self.current_distance < self.red_safety_dist:
            cx = red_target['cx']
            cy = red_target['cy']
            x, y, w, h = red_target['box']
            text_color = red_target['text_color']

            pixel_error = image_center_x - cx
            normalized_error = pixel_error / image_center_x

            cv2.rectangle(frame, (x, y), (x + w, y + h), text_color, 2)
            cv2.circle(frame, (cx, cy), 6, (255, 255, 255), -1)

            raw_turn = self.kp_angular * normalized_error
            target_aligned = abs(normalized_error) < self.align_tolerance

            if not target_aligned:
                twist.linear.x = 0.0
                twist.angular.z = max(min(raw_turn, self.max_angular_vel), -self.max_angular_vel)
                status_txt = "RED CRITICAL: ALIGNING TO RETREAT"
            else:
                dist_error = self.current_distance - self.red_safety_dist
                twist.linear.x = max(min(dist_error * 0.3, self.forward_speed), -self.forward_speed)
                twist.angular.z = 0.0
                status_txt = f"RED TOO CLOSE: BACKING AWAY ({self.current_distance:.2f}m)"

        # --- CONDITION 2: GREEN CENTERING & APPROACH PIPELINE ---
        # Executes your original workflow layout logic
        elif green_target is not None:
            cx = green_target['cx']
            cy = green_target['cy']
            x, y, w, h = green_target['box']
            text_color = green_target['text_color']

            pixel_error = image_center_x - cx
            normalized_error = pixel_error / image_center_x

            # Draw Green Indicators
            cv2.rectangle(frame, (x, y), (x + w, y + h), text_color, 2)
            cv2.circle(frame, (cx, cy), 6, (255, 255, 255), -1)

            # Draw a passive Red tracking overlay if Red is visible but far away
            if red_target is not None:
                rx, ry, rw, rh = red_target['box']
                cv2.rectangle(frame, (rx, ry), (rx + rw, ry + rh), (0, 0, 100), 1)

            raw_turn = self.kp_angular * normalized_error
            target_aligned = abs(normalized_error) < self.align_tolerance

            # STEP 1: Always rotate to bring centroid into focus first
            if not target_aligned:
                twist.linear.x = 0.0
                twist.angular.z = max(min(raw_turn, self.max_angular_vel), -self.max_angular_vel)
                status_txt = "GREEN TRACKED: CENTERING CENTROID"
            else:
                # STEP 2: Once centered, look at the LiDAR range to determine stopping profile
                if self.current_distance <= self.green_stop_dist:
                    twist.linear.x = 0.0
                    twist.angular.z = 0.0
                    status_txt = f"GREEN REACHED: LOCKED AT {self.current_distance:.2f}m"
                else:
                    twist.linear.x = self.forward_speed  
                    twist.angular.z = 0.0
                    status_txt = f"GREEN CENTERED: APPROACHING (Dist: {self.current_distance:.2f}m)"

        # --- CONDITION 3: DEFAULT HUNTING ROTATION ---
        else:
            if red_target is not None:
                rx, ry, rw, rh = red_target['box']
                cv2.rectangle(frame, (rx, ry), (rx + rw, ry + rh), (0, 0, 100), 1)
                
            twist.linear.x = 0.0
            twist.angular.z = 0.16
            status_txt = "HUNTING GREEN: SPINNING..."

        # UI Overlay
        cv2.line(frame, (int(image_center_x), 0), (int(image_center_x), height), (255, 255, 0), 2)
        cv2.putText(frame, status_txt, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # Publish commands
        self.cmd_pub.publish(twist)
        cv2.imshow("Tracking", frame)
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
