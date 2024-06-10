import rclpy
from rclpy.node import Node
from gazebo_msgs.srv import SpawnEntity
import os

class SpawnRoverNode(Node):
    def __init__(self):
        super().__init__('spawn_rover')
        self.cli = self.create_client(SpawnEntity, '/spawn_entity')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting again...')
        self.spawn_rover()

    def spawn_rover(self):
        req = SpawnEntity.Request()
        sdf_file_path = os.path.join(
            os.path.dirname(__file__),
            '../models/rover.sdf'
        )

        with open(sdf_file_path, 'r') as sdf_file:
            req.xml = sdf_file.read()

        req.name = 'rover'
        req.robot_namespace = ''
        req.initial_pose.position.x = 0.0
        req.initial_pose.position.y = 0.0
        req.initial_pose.position.z = 0.0

        future = self.cli.call_async(req)
        future.add_done_callback(self.spawn_callback)

    def spawn_callback(self, future):
        try:
            response = future.result()
            self.get_logger().info(f'Spawn status: {response.status_message}')
        except Exception as e:
            self.get_logger().error(f'Exception while calling service: {e}')

def main(args=None):
    rclpy.init(args=args)
    node = SpawnRoverNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

