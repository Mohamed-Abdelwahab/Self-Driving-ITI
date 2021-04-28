#!/usr/bin/env python3

import rclpy

from rclpy.node import Node
from example_interfaces.msg import Int64
from example_interfaces.srv import SetBool


#inherit from Node
class my_node(Node):
    def __init__(self):
        super().__init__("node2")
        self.obj_pub = self.create_publisher(Int64,"counter",10)
        
        self.create_subscription(Int64,"int_num",self.callback,10)
        # create ros service (type,name,callback)
        self.create_service(SetBool,"reset_client",self.srv_call)
        self.sum = 0
        
        #self.get_logger().info("sub node is started now")

    def callback(self,msg):
        #self.get_logger().info(f"{msg.data}")
        self.sum += msg.data
        x = Int64()
        x.data = self.sum
        self.obj_pub.publish(x)
            
        self.get_logger().info(f"{x.data}")

    def srv_call(self,req,resp):

        # 4) extract memebers of request 
        req = req.data
        
        if req == True:
            resp.success = True
            resp.message = "reset done "
            self.sum = 0



        # 5) process the data to calculate response
        
        # print response 
        #self.get_logger().info(str(rsp.sum))
        # 6) return response
        return resp

       



def main(args=None):
    rclpy.init(args=args)

    node = my_node()
    rclpy.spin(node)
    



    rclpy.shutdown()


if __name__ == "__main__":
    main()




