#!/usr/bin/env python3

import rclpy

from rclpy.node import Node
from my_msgs.msg import Newms
from example_interfaces.msg import Int64
from my_msgs.srv import Newsr


#inherit from Node
class my_node(Node):
    def __init__(self):
        super().__init__("sub_node")
        self.create_subscription(Newms,"new_topic",self.callback,10)
        self.pub = self.create_publisher(Int64, "counter", 10)
        self.create_service(Newsr, "reset_counter", self.callback2)
        self.get_logger().info("sub node is started now")
        self.counter = 0

    def callback(self,msg):
        

        x = Int64()
        x.data = self.counter
        self.pub.publish(x)
        self.counter += msg.num
       
    def callback2(self,rq,rs):

        if rq.flag == True:

            self.counter = 0 
            rs.message = "Done reset"
            return rs
        rs.message = "Didn't reset"
        return rs


def main(args=None):
    rclpy.init(args=args)

    node = my_node()
    rclpy.spin(node)
    

    rclpy.shutdown()


if __name__ == "__main__":
    main()






