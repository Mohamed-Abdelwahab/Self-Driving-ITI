#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

# 1) import message/service types 
from example_interfaces.srv import SetBool

class myClient(Node):
    def __init__(self):
        # node name  should be (unique)
        super().__init__("Client_node")

        # 2) send request by calling service_client with reqeust values as
        # arguments (arg1,arg2,..)
        self.service_client(True)
        


    # 3) define service_client fuction with inputs = variables of request
    def service_client(self,a):
        # 4) create client object create_client(type,service_name) 
        client=self.create_client(SetBool,"reset_client")

        # 5) wait for service to run 
        while client.wait_for_service(0.25)==False:
            self.get_logger().warn("wating for server")

        # 6) create a request object to fill its members
        request = SetBool.Request()
        # 7) fill request attributes/variables with values
        request.data = a
        

        # 8) send service request and execute callback when getting result
        futur_obj = client.call_async(request)
        futur_obj.add_done_callback(self.future_call)

    # 9) define callback withe response as input
    def future_call(self,future_msg):
        self.get_logger().info(str(future_msg.result().message))
        


       


def main (args=None):
    # 10) start communication
    rclpy.init(args=args)
    # 11) create object from my node
    node1 = myClient()
    # keep the node running
    rclpy.spin(node1)
    rclpy.shutdown()

if __name__ == "__main__":
    main()

# 12) don't forget to updte setup.py file