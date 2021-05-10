#!/usr/bin/env python3

# 1) import ros client library 
import rclpy
from rclpy.node import Node
# 2) import message/service types 
from turtlesim.msg import Pose
 
#inherit from Node
class my_node(Node):
    def __init__(self):
        # node name  should be (unique)
        super().__init__("sub_node")
        # 3) create subscriber object (type,topic_name,callback,queue_size)
        self.create_subscription(Pose,"turtle1/custom_pose",self.callback,rclpy.qos.qos_profile_sensor_data  )
        
        self.get_logger().info("sub node is started now")

    # 4) define callback function called when recieving message from a topic
    def callback(self,msg):

        # 5) access message members msg.data
        #self.get_logger().info(f"{msg.x},{msg.y}")
        print(f"{msg.x},{msg.y}")
       



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


 