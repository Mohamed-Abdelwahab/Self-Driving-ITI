#!/usr/bin/env python3

import rclpy
import numpy as np
from rclpy.node import Node
from sensor_msgs.msg import Imu
from functions import quaternion_from_euler,euler_from_quaternion


class my_node(Node):
    def __init__(self):
        super().__init__("node1")

        # create subscriber to /imu topic
        self.create_subscription(Imu,"imu",self.imu_callback,rclpy.qos.qos_profile_sensor_data)
        
    
    def imu_callback(self,msg):


        # get data from IMU

        #self.get_logger().info(msg.header.frame_id)
        #self.get_logger().info(str(msg.header.stamp))
        
        # orientation in quaternion , convert to euler 

        roll, pitch, yaw = euler_from_quaternion(self,msg.orientation)
        #convert to degree
        yaw_deg = np.rad2deg(yaw)

        if -2 < abs(yaw_deg) < 2 :
            self.get_logger().info(f"“The robot is nearly heading north .. Heading is: {yaw_deg} degrees”")
        
        if abs( msg.linear_acceleration.x) > .3 :
            self.get_logger().warn(f'Warning !! .. linear acceleration x exceeded the limit . Current acceleration is \
                {msg.linear_acceleration.x} m/s^2')

        if abs(msg.angular_velocity.z > .3 ):
            self.get_logger().warn(f'Warning !! .. angular acceleration x exceeded the limit . Current acceleration is \
                {msg.angular_velocity.z} m/s^2')


            
        



def main(args = None):
    rclpy.init(args=args)

    node = my_node()

    rclpy.spin(node)

    rclpy.shutdown()
    

if __name__ == "__main__":
    main()

  


