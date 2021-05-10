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
        super().__init__("sub_node")
        # 3) create subscriber object (type,topic_name,callback,queue_size)
        self.create_subscription(String,"my_topic",self.callback,rclpy.qos.qos_profile_sensor_data  )
        
        self.get_logger().info("sub node is started now")

        self.counter = 0

    # 4) define callback function called when recieving message from a topic
    def callback(self,msg):

        # 5) access message members msg.data
        self.get_logger().info(f"Mohamed Abdelwahab heard : {msg.data} , {self.counter}")
        self.counter += 1 
       



def main(args=None):
    # 6) start communication
    rclpy.init(args=args)
    # 7) create object from my node
    node = my_node()
    # keep the node running
    rclpy.spin(node)
    



    rclpy.shutdown()


if __name__ == "__main__":
    main()
# 8) don't forget to updte setup.py file





