#!/usr/bin/env python3

import rclpy

from rclpy.node import Node
from my_msgs.msg import Newms


#inherit from Node
class my_node(Node):
    def __init__(self):
        super().__init__("pub_node")
        self.create_timer(.5,self.callback)
        self.obj_pub = self.create_publisher(Newms,"new_topic",10)
        self.get_logger().info("node is started now")
        self.counter = 0

    def callback(self):
        #self.get_logger().info("Mohamed Abdelwahab 12345")
        msg = Newms()
        msg.message = "Mohamed Abdelwahab is publishing : 5 "
        msg.num = 5
        
        
        self.obj_pub.publish(msg)




def main(args=None):
    rclpy.init(args=args)

    node = my_node()
    rclpy.spin(node)
    



    rclpy.shutdown()


if __name__ == "__main__":
    main()






