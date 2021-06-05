#!/usr/bin/env python3
import rclpy
import time
import numpy as np 
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


laser_data =[]
v_x = 0.0
w_z = 0.0


class Control(Node):
    def __init__(self):
    
        super().__init__("control_node")

        # create sub object to key_cmd_vel
        self.create_subscription(Twist, "key_cmd_vel", self.key_callback, 10) 
        # create sub object to scan 
        self.create_subscription(LaserScan,"scan",self.scan_callback, rclpy.qos.qos_profile_sensor_data)
        # create pub object to cmd_vel
        self.pub = self.create_publisher(Twist,"cmd_vel",10)
    
   

   
    def scan_callback(self,message):

        global laser_data,v_x,w_z
        laser_data = message.ranges
        #print(laser_data[0])
       
        # create message object to send control commands 
        control = Twist()
        # fill message fields
        control.linear.y = 0.0
        control.linear.z = 0.0
        control.angular.x = 0.0
        control.angular.y = 0.0
        control.angular.z = w_z
        self.pub.publish(control)

        # check moving forward
        if v_x > 0:
            #check distance in front of the robot 
            #min_value = laser_data[0]
            # get min distance in range +- 20 deg 
            min_value = min (min(laser_data[0:20]),min(laser_data[-20:-1]))
            #print(min_value)

            # stop if min distance = .7
            if min_value < .7:
                control.linear.x = 0.0 
                control.angular.z = w_z
                self.pub.publish(control)
            # move with normal speed if your distance > 3 m 
            elif min_value > 3.0 :
                control.linear.x = v_x
                control.angular.z = w_z
                self.pub.publish(control)
            # slow down if 3 > distance to obstacle > .5
            elif min_value > .5 :
                control.linear.x = (v_x * min_value) / 3.0
                control.angular.z = w_z
                self.pub.publish(control)
            
        else:
            control.linear.x = v_x
            control.angular.y = w_z
            self.pub.publish(control)

    def key_callback(self,twist):

        global v_x,w_z
       
        # get velocity from keyboard
        v_x = twist.linear.x
        w_z = twist.angular.z 

        
        

def main (args=None):
    
    rclpy.init(args=args)
    # create object from my node
    node = Control()
    # keep the node running
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
    

