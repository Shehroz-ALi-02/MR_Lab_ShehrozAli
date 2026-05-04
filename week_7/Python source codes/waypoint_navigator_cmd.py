import sys
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from nav2_msgs.action import FollowWaypoints
from geometry_msgs.msg import PoseStamped

class DynamicNavigator(Node):
    def __init__(self):
        super().__init__('dynamic_navigator')
        self._client = ActionClient(self, FollowWaypoints, 'follow_waypoints')

    def send_waypoints(self, waypoints):
        self.get_logger().info('Waiting for FollowWaypoints action server...')
        self._client.wait_for_server()

        goal_msg = FollowWaypoints.Goal()
        goal_msg.poses = waypoints

        self.get_logger().info(f'Sending {len(waypoints)} dynamic waypoints...')
        
        send_goal_future = self._client.send_goal_async(goal_msg)
        rclpy.spin_until_future_complete(self, send_goal_future)
        
        goal_handle = send_goal_future.result()
        if not goal_handle.accepted:
            self.get_logger().error('Goal rejected!')
            return

        self.get_logger().info('Navigating to waypoints...')
        result_future = goal_handle.get_result_async()
        rclpy.spin_until_future_complete(self, result_future)
        self.get_logger().info('Mission Complete!')

def make_pose(x, y, w):
    pose = PoseStamped()
    pose.header.frame_id = 'map'
    pose.pose.position.x = float(x)
    pose.pose.position.y = float(y)
    pose.pose.orientation.w = float(w)
    return pose

def main():
    rclpy.init()
    
    # Get all arguments after the filename
    args = sys.argv[1:]
    
    # Check if we have groups of 3 (x, y, w)
    if len(args) == 0 or len(args) % 3 != 0:
        print("Usage: python3 dynamic_waypoint_navigator.py x1 y1 w1 x2 y2 w2 ...")
        print("Example: python3 dynamic_waypoint_navigator.py 1.0 0.5 1.0 2.0 -1.0 1.0")
        return

    waypoints = []
    for i in range(0, len(args), 3):
        x = args[i]
        y = args[i+1]
        w = args[i+2]
        waypoints.append(make_pose(x, y, w))

    navigator = DynamicNavigator()
    navigator.send_waypoints(waypoints)
    
    navigator.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
