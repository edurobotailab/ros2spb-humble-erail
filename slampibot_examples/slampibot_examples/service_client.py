import sys
import rclpy
from rclpy.node import Node
from slampibot_interfaces.srv import AddTwoInts


class ServiceClient(Node):

    def __init__(self, a, b):
        super().__init__("service_client")
        self.client_ = self.create_client(AddTwoInts, "add_two_ints")

        while not self.client_.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("service not available, waiting again...")
        
        self.req_ = AddTwoInts.Request()
        self.req_.a = a
        self.req_.b = b
        self.future_ = self.client_.call_async(self.req_)
        self.future_.add_done_callback(self.responseCallback)

    def responseCallback(self, future):
        self.get_logger().info('Service Response %d' % future.result().sum)        

def main():
    rclpy.init()
    
    if len(sys.argv) != 3:
        print("Wrong number of arguments! Usage: service_client A B")
        return -1

    service_client = ServiceClient(int(sys.argv[1]), int(sys.argv[2]))
    rclpy.spin(service_client)
    service_client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()