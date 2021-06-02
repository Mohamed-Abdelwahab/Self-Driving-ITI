#!/usr/bin/env python3

import rclpy
import time 
import numpy as np
from rclpy.node import Node
from nav_msgs.msg import Path
from example_interfaces.msg import String
from functions import menger_curvature



class my_node(Node):
    def __init__(self):
        super().__init__("curve_node")

        # create subscriber to /imu topic
        self.create_subscription(Path,"plan",self.plan_callback,10)
        self.pub = self.create_publisher(String,"str_topic",10)
    def plan_callback(self,msg):

        plan_size = len(msg.poses)
        intrval = int(plan_size/10)

        point_1_x = msg.poses[0].pose.position.x
        point_1_y = msg.poses[0].pose.position.y
        point_2_x = msg.poses[intrval].pose.position.x 
        point_2_y = msg.poses[intrval].pose.position.y
        point_3_x = msg.poses[2*intrval].pose.position.x
        point_3_y = msg.poses[2*intrval].pose.position.y 

        curvature = menger_curvature(self, point_1_x, point_1_y, point_2_x, point_2_y, point_3_x, point_3_y)
        #self.get_logger().info(str(curvature))
        message = String()
        if curvature < 1 :   
            message.data = "The path is straight"
        else:
            message.data = f"The robot is turning with a curvature {curvature} where c is the curvature of the path."
        self.pub.publish(message)

def main(args = None):
    rclpy.init(args=args)

    node = my_node()

    rclpy.spin(node)

    rclpy.shutdown()
    

if __name__ == "__main__":
    main()
