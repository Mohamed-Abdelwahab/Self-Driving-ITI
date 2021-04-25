#!/usr/bin/env python3

import rclpy

from rclpy.node import Node
from example_interfaces.msg import String
from example_interfaces.msg import Int16

#inherit from Node
class my_node(Node):
    def __init__(self):
        super().__init__("my_node")
        self.create_timer(.5,self.callback)
        self.obj_pub = self.create_publisher(String,"str_topic",10)
        
        #self.get_logger().info("node is started now")
        self.counter = 0

    def callback(self):


        self.get_logger().info(f"Mohamed is publish , {self.counter}")
        self.counter += 1
        self.create_subscription(Int16,"reset_flag",self.callback2,10)
        
        msg = String()
        msg.data = f"Mohamed is publish , {self.counter}"
        self.obj_pub.publish(msg)
        
        

    def callback2(self,data):

        self.counter = data.data
        




def main(args=None):
    rclpy.init(args=args)

    node = my_node()
    rclpy.spin(node)
    



    rclpy.shutdown()


if __name__ == "__main__":
    main()



