#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

# 1) import message/service types 
from std_srvs.srv import Empty


class myClient(Node):
    def __init__(self):
        # node name  should be (unique)
        super().__init__("Client_node")

        # 2) send request by calling service_client with reqeust values as
        # arguments (arg1,arg2,..)
        self.service_client()
        


    # 3) define service_client fuction with inputs = variables of request
    def service_client(self):
        # 4) create client object create_client(type,service_name) 
        client=self.create_client(Empty,"reset")

        # 5) wait for service to run 
        while client.wait_for_service(0.25)==False:
            self.get_logger().warn("wating for server")

        # 6) create a request object to fill its members
        request = Empty.Request()
        
        

        # 7) send service request and execute callback when getting result
        futur_obj = client.call_async(request)
        futur_obj.add_done_callback(self.future_call)

    # 8) define callback withe response as input
    def future_call(self,future_msg):
        self.get_logger().info("Done")
        


       


def main (args=None):
    
    rclpy.init(args=args)
    node1 = myClient()
    rclpy.spin(node1)
    rclpy.shutdown()

if __name__ == "__main__":
    main()

