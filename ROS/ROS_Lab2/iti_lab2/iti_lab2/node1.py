#!/usr/bin/env python3

# 1) import ros client library 
import rclpy
from rclpy.node import Node
# 2) import message/service types 
from example_interfaces.msg import Int64


#inherit from Node
class my_node(Node):
    def __init__(self):
        # node name  should be (unique)
        super().__init__("pub_int_node")
        # 3) create publisher object (type,topic_name,queue_size)
        self.obj_pub = self.create_publisher(Int64,"int_num",10)
        # 4) create timer to control publishing rate (freq,callback)
        self.create_timer(.5,self.callback)
        self.get_logger().info("node is started now")

    # 5) define callback function  
    def callback(self):
        #self.get_logger().info("Mohamed Abdelwahab 12345")
        # 6) create message object  
        msg = Int64()
        # 7) fill message data
        msg.data = 5
        # 8) publish message
        self.obj_pub.publish(msg)




def main(args=None):
    # 9) start communication
    rclpy.init(args=args)
    # 10) create object from my node
    node = my_node()
    # keep the node running
    rclpy.spin(node)
    



    rclpy.shutdown()


if __name__ == "__main__":
    main()
# 11) don't forget to updte setup.py file



