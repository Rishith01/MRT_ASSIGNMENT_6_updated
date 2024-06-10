import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped

class MoveInCircle(Node):

    def __init__(self):
        super().__init__('move_in_circle')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.path_publisher_ = self.create_publisher(Path, '/path', 10)
        self.timer = self.create_timer(0.1, self.publish_twist)
        self.circle_radius = 1.0
        self.angular_speed = 0.1
        self.linear_speed = self.angular_speed * self.circle_radius

        self.twist_msg = Twist()
        self.twist_msg.linear.x = self.linear_speed
        self.twist_msg.angular.z = self.angular_speed

        self.path_msg = Path()
        self.pose_stamped = PoseStamped()
        self.pose_stamped.pose.position.x = self.circle_radius
        self.pose_stamped.pose.position.y = 0.0
        self.pose_stamped.pose.orientation.w = 1.0
        self.path_msg.poses.append(self.pose_stamped)

    def publish_twist(self):
        self.publisher_.publish(self.twist_msg)
        self.path_publisher_.publish(self.path_msg)

def main(args=None):
    rclpy.init(args=args)
    move_in_circle = MoveInCircle()
    rclpy.spin(move_in_circle)
    move_in_circle.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
