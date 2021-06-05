#!/usr/bin/env python3

import rclpy
import time 
import numpy as np
from rclpy.node import Node
from nav_msgs.msg import Path
from example_interfaces.msg import String
from functions import menger_curvature , euler_from_quaternion



class my_node(Node):
    def __init__(self):
        super().__init__("curve_node")

        # create subscriber to /imu topic
        self.create_subscription(Path,"local_plan",self.plan_callback,10)
        self.pub = self.create_publisher(String,"str_topic",10)
    def plan_callback(self,msg):

        plan_size = len(msg.poses)
        intrval = int(plan_size/3)
        #self.get_logger().info(str(plan_size))
        point_1_x = msg.poses[0].pose.position.x
        point_1_y = msg.poses[0].pose.position.y
        point_2_x = msg.poses[intrval].pose.position.x 
        point_2_y = msg.poses[intrval].pose.position.y
        point_3_x = msg.poses[2*intrval].pose.position.x
        point_3_y = msg.poses[2*intrval].pose.position.y 

        #Get orientation of the fiest and last  points 
        r0,p0,y0 = euler_from_quaternion(self, msg.poses[0].pose.orientation)
        r1,p1,y1 = euler_from_quaternion(self, msg.poses[-1].pose.orientation)
     
        ang_diff = y1 - y0 

        #self.get_logger().info(str(ang_diff))

        

        ##__________________________Method(1)__________________________________##
       
        if .44 >=ang_diff >= 0.268:
            curvature = menger_curvature(self, point_1_x, point_1_y, point_2_x, point_2_y, point_3_x, point_3_y)
            self.get_logger().info( f"The robot is turning left with a curvature {curvature} where c is the curvature of the path.")
        if -.44 <=ang_diff <= -0.268:
            curvature = menger_curvature(self, point_1_x, point_1_y, point_2_x, point_2_y, point_3_x, point_3_y)
            self.get_logger().info( f"The robot is turning right with a curvature {curvature} where c is the curvature of the path.")
        else:
            self.get_logger().info("The path is straight")
        ##__________________________Method(2)__________________________________##

        # curvature = menger_curvature(self, point_1_x, point_1_y, point_2_x, point_2_y, point_3_x, point_3_y)
        # #self.get_logger().info(str(curvature))
        
        # if curvature < 1 :   
        #     self.get_logger().info("The path is straight")
        # else:
        #     if ang_diff > 0:
        #         self.get_logger().info( f"The robot is turning left with a curvature {curvature} where c is the curvature of the path.")
        #     else:
        #         self.get_logger().info(f"The robot is turning right with a curvature {curvature} where c is the curvature of the path.")
        

def main(args = None):
    rclpy.init(args=args)

    node = my_node()

    rclpy.spin(node)

    rclpy.shutdown()
    

if __name__ == "__main__":
    main()