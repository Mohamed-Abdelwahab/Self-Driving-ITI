#!/usr/bin/env python3

import rclpy
import time 
import numpy as np
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

## linear error , linear error diffrence , linear error integeral 
e_l = 0.0
e_dot_l = 0.0
E_l = 0.0 
e_old_l = 0.0
## linear error , linear error diffrence , linear error integeral 
e_a = 0.0          # error of angel
e_dot_a = 0.0      # diffrence of angular error 
E_a = 0.0          # sum of angular error 
E_plod_a = 0.0
e_old_a = 0.0
##________________________control variables____________________##
# linear pid control variables
kp_l = .1 
ki_l = .001
kd_l = .005
# linear pid control variables
kp_a = 1 
ki_a = .005
kd_a = .1




# goal position
x = 0
y = 0 
error = .01 


class my_node(Node):
    def __init__(self):
        super().__init__("node1")

        self.current_x = 0
        self.current_y = 0 
        self.current_angel = 0
        self.linear_velocity = 0
        self.angular_velocity = 0

        # create sub object to pose topic to get current state of the robot
        self.create_subscription(Pose, "/turtle1/pose", self.pose_callback, 10) 

        # create pub object to send control commands to the robot
        self.pub = self.create_publisher(Twist,"/turtle1/cmd_vel",10)
        

    def pose_callback(self,pose):

        global  x,y,error
        
        # get current state of robot 
        self.current_x = pose.x
        self.current_y = pose.y  
        self.current_angel = pose.theta
        self.linear_velocity = pose.linear_velocity
        self.angular_velocity = pose.angular_velocity
	
	# execute go to goal position 
        self.go_to_goal( x,y,error)


    # Get ecludian distance between 2 points 
    def get_distance(self,x1,y1,x2,y2):
        return np.sqrt(np.power((x1-x2),2) + np.power((y1-y2),2))


    def go_to_goal(self,x,y,error):

        global e_l,e_a,e_dot_l,e_dot_a,E_l,E_a,e_old_a,e_old_l
        # create message object to send control commands 
        control = Twist()
        # fill message fields
        control.linear.y = 0.0
        control.linear.z = 0.0
        control.angular.x = 0.0
        control.angular.y = 0.0

	# calculate PID for linear velocity
	# 1- current error
        e_l = (self.get_distance(x, y, self.current_x, self.current_y))
        # 2- error diffrence
        e_dot_l = e_l - e_old_l
        # 3- error sum
        E_l += e_l 
        # 4- controller output
        u_l = kp_l*e_l + ki_l*E_l + kd_l*e_dot_l
        # set old error to current error
        e_old_l = e_l 

        

	# calculate PID for angular velocity
	# 1- current error in angels 
        e_a = ( np.arctan2((y - self.current_y),(x - self.current_x))- self.current_angel)
        # 2- error diffrence
        e_dot_a = e_a - e_old_a
        # 3- error sum
        E_a += e_a 
        # 4- controller output
        u_a = kp_a*e_a + ki_a*E_a + kd_a*e_dot_a
        # set old error to current error
        e_old_l = e_l
        
        # send linear velocity which proportional with distance between current and goal position
        control.linear.x = u_l
        # send angular velocity which proportional with diffrence between current and goal orientation
        control.angular.z = u_a
        # publish te message 
        self.pub.publish(control)
            # check if the error between current and goal position < tolerance 
        if self.get_distance(x, y, self.current_x, self.current_y) < error:
            control.linear.x = 0.0
            control.angular.z = 0.0
            self.pub.publish(control)

            


        

    


    
def main(args = None):

    global x,y,error

    # get goal position from the user 
    x = float(input("Enter goal x position : "))
    y = float(input("Enter goal y position : "))
    error = bool(input("Enter tolerance value : "))
    rclpy.init(args=args)

    node = my_node()

    rclpy.spin(node)

    rclpy.shutdown()
    

if __name__ == "__main__":

    main()
