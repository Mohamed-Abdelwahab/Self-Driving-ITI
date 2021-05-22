#!/usr/bin/env python3

import rclpy
import numpy as np
from rclpy.node import Node
from nav_msgs.msg import Odometry
from functions import quaternion_from_euler,euler_from_quaternion

# read from file
f = open("pose.csv",'r')
v = []
for line in f:
    
    v.append(line[:-1].split(','))
    
class my_node(Node):
    def __init__(self):
        super().__init__("node1")

        # create subscriber to /odom topic
        self.create_subscription(Odometry,"odom",self.odom_callback,rclpy.qos.qos_profile_sensor_data)

        self.i = 3
        
    
    def odom_callback(self,odom):

        # Get Position (x,y,z)
        act_x = odom.pose.pose.position.x 
        act_y = odom.pose.pose.position.y
        act_z = odom.pose.pose.position.z  

        # Get Orientation in roll, pitch, yaw
        roll, pitch, yaw = euler_from_quaternion(self,odom.pose.pose.orientation)
        
        #convert to degree
        act_yaw_deg = np.rad2deg(yaw)

        # calculate error
        x_error = float(v[self.i][0]) - act_x
        y_error = float(v[self.i][1]) - act_y
        yaw_error = float(v[self.i][2]) - act_yaw_deg


        self.get_logger().info(f"you are currently at x: {act_x},y: {act_y},yaw:{act_yaw_deg}.\
                Go To (goall_x : {v[self.i][0]},goal_y:{v[self.i][1]},goal_z:{float(v[self.i][2])})")

        if self.i == len(v)-1:
            if x_error < .5 and y_error < .5 and yaw_error < 5:
                self.get_logger().info (f"i execute all {self.i } position and last one is x:{v[self.i][0]}\
                    ,y:{v[self.i][1]}, theta:{float(v[self.i][2])}")


        if self.i < len(v)-1:
            
            #check tolerance
            if x_error < .5 and y_error < .5 and yaw_error < 5:
                self.get_logger().info(f"I reached goal{self.i} with x:{v[self.i][0]} ,y:{v[self.i][1]} \
                    .Go To (new_x : {v[self.i+1][0]},new_y:{v[self.i+1][1]}) ")
                self.i += 1

        
                

        

        # Get Orientation in quaternion (x,y,z,w)
        # self.get_logger().info(str(odom.pose.pose.orientation.x ) + "\n")
        # self.get_logger().info(str(odom.pose.pose.orientation.y) + "\n")
        # self.get_logger().info(str(odom.pose.pose.orientation.z ) + "\n")
        # self.get_logger().info(str(odom.pose.pose.orientation.w ) + "\n")

        # Get Linear velocity 
        # self.get_logger().info(str(odom.twist.twist.linear.x ) + "\n")
        # self.get_logger().info(str(odom.twist.twist.linear.y) + "\n")
        # self.get_logger().info(str(odom.twist.twist.linear.z ) + "\n")

        # Get Angular velocity 
        # self.get_logger().info(str(odom.twist.twist.angular.x ) + "\n")
        # self.get_logger().info(str(odom.twist.twist.angular.y) + "\n")
        # self.get_logger().info(str(odom.twist.twist.angular.z ) + "\n")

        # # Get name of parent frame & child frame & time 

        # # parent frame
        # self.get_logger().info(odom.header.frame_id )

        # # child frame
        # self.get_logger().info(odom.child_frame_id)

        # # time stamp
        # self.get_logger().info(str(odom.header.stamp))



def main(args = None):
    rclpy.init(args=args)

    node = my_node()

    rclpy.spin(node)

    rclpy.shutdown()
    

if __name__ == "__main__":
    main()

    
