#!/usr/bin/env python3

import rclpy

from rclpy.node import Node
from example_interfaces.msg import String
from example_interfaces.msg import Int16


#inherit from Node
class my_node(Node):
    def __init__(self):
        super().__init__("sub_node")
        self.obj_pub2 = self.create_publisher(Int16,"number",10)
        self.obj_pub = self.create_publisher(Int16,"reset_flag",10)
        self.create_subscription(String,"str_topic",self.callback,10)
        
        #self.get_logger().info("sub node is started now")

    def callback(self,msg):
        #self.get_logger().info(msg.data)
        
        
        x = Int16()
        y = Int16()
        z = Int16()
        y.data = 0
        x.data = int(msg.data.split()[-1])
        z.data = int(int(msg.data.split()[-1]) - 1)
        #self.get_logger().info(f"{ x.data}")
        self.obj_pub2.publish(z)
        if x.data >= 6:
            self.obj_pub.publish(y)
            
            #self.get_logger().info(f"{ x.data}")

       



def main(args=None):
    rclpy.init(args=args)

    node = my_node()
    rclpy.spin(node)
    



    rclpy.shutdown()


if __name__ == "__main__":
    main()





