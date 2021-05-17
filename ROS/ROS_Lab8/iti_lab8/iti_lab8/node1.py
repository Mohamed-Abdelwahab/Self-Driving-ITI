#!/usr/bin/env python3

# 1) import ros client library 
import rclpy
from rclpy.node import Node
# 2) import message/service types 
from example_interfaces.msg import String


#inherit from Node
class my_node(Node):
    def __init__(self):
        # node name  should be (unique)
        super().__init__("my_node")
        # 3) create publisher object (type,topic_name,queue_size)
        self.obj_pub = self.create_publisher(String,"str_topic",10)
        # 4) create timer to control publishing rate (freq,callback)
        self.create_timer(1/1,self.callback)
        self.get_logger().info("node is started now")
        self.i = 0

    # 5) define callback function  
    def callback(self):
        
        # 6) create message object  
        msg = String()
        # 7) fill message data

        if self.i % 2 == 0 :
            msg.data = "Hi"
            self.i += 1
        else:
            msg.data = "Hello"
            self.i += 1

        
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




