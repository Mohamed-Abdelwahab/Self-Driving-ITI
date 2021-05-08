#!/usr/bin/env python3

import rclpy
import time 
import numpy as np
from rclpy.node import Node
from turtlesim.msg import Pose
from turtlesim.srv import Kill
from turtlesim.srv import Spawn
from geometry_msgs.msg import Twist
from example_interfaces.msg import Bool


x = 0
y = 0 
error = 0.01


class my_node(Node):
    def __init__(self):
        super().__init__("node1")

        self.current_x = 0
        self.current_y = 0 
        self.current_angel = 0
        self.linear_velocity = 0
        self.angular_velocity = 0

        # self.x = float(np.random.randint(1,11))
        # self.y = float(np.random.randint(1,11))
        # self.theta = float(np.random.randint(0,np.pi))
        # self.spawn_client(self.x,self.y,self.theta,"Moha")


        # create sub object to pose topic to get current state of the robot
        self.create_subscription(Pose, "turtle1/pose", self.pose_callback, 10) 
        #self.create_subscription(Pose, "position", self.sub_callback, 10)
        self.create_subscription(Pose, "Moha/pose", self.sub_callback, 10)
        # create pub object to send control commands to the robot
        self.pub = self.create_publisher(Twist,"/turtle1/cmd_vel",10)
        # published to restart new turtle 
        self.pub2 = self.create_publisher(Bool, "flag", 10)
        
        # create timer to control publishing rate 
       # self.create_timer(1/1, self.callback )        
        



    # def spawn_client(self,x,y,theta,name):
    #     #  create client object create_client(type,service_name) 
    #     client = self.create_client(Spawn,"spawn")

    #     #  wait for service to run 
    #     while client.wait_for_service(0.25)==False:
    #         self.get_logger().warn("wating for server")

    #     # create a request object to fill its members
    #     request = Spawn.Request()
    #     #  fill request attributes/variables with values
    #     request.name = name 
    #     request.x = x
    #     request.y = y
    #     request.theta = theta

    #     #  send service request and execute callback when getting result
    #     futur_obj = client.call_async(request)
    #     futur_obj.add_done_callback(self.spawn_response_call)

    # #  define callback with response as input
    # def spawn_response_call(self,future_msg):
    #     self.get_logger().info("Done")

    def kill_client(self,name):
        #  create client object create_client(type,service_name) 
        client = self.create_client(Kill,"kill")

        #  wait for service to run 
        while client.wait_for_service(0.25)==False:
            self.get_logger().warn("wating for server")

        # create a request object to fill its members
        request = Kill.Request()
        #  fill request attributes/variables with values
        request.name = name 
        # request.b = b

        #  send service request and execute callback when getting result
        futur_obj = client.call_async(request)
        futur_obj.add_done_callback(self.kill_response_call)

    #  define callback with response as input
    def kill_response_call(self,future_msg):

        flag = Bool()
        flag.data = True
        self.pub2.publish(flag)

    # subscribe to turtle 2 position 
    def sub_callback(self,msg):
        global x,y
        x = msg.x
        y = msg.y

    # subscribe to current turtle pose
    def pose_callback(self,pose):

        global  x,y,error

        self.current_x = pose.x
        self.current_y = pose.y  
        self.current_angel = pose.theta
        self.linear_velocity = pose.linear_velocity
        self.angular_velocity = pose.angular_velocity

        self.go_to_goal( x,y,error)


    # Get ecludian distance between 2 points 
    def get_distance(self,x1,y1,x2,y2):
        return np.sqrt(np.power((x1-x2),2) + np.power((y1-y2),2))


    def go_to_goal(self,x,y,error):

        # create message object to send control commands 
        control = Twist()
        # fill message fields
        control.linear.y = 0.0
        control.linear.z = 0.0
        control.angular.x = 0.0
        control.angular.y = 0.0

        

            # send linear velocity which proportional with distance between current and goal position
        control.linear.x = .5 * (self.get_distance(x, y, self.current_x, self.current_y))
            # send angular velocity which proportional with diffrence between current and goal orientation
        control.angular.z = 4*( np.arctan2((y - self.current_y),(x - self.current_x))- self.current_angel)
            # publish the message
        self.pub.publish(control)
            # check if the error between current and goal position < tolerance 
        if self.get_distance(x, y, self.current_x, self.current_y) < error:
            control.linear.x = 0.0
            control.angular.z = 0.0
            self.pub.publish(control)
            self.kill_client("Moha")
    

    



    
def main(args = None):

    # global x,y,error

    # x = float(input("Enter goal x position : "))
    # y = float(input("Enter goal y position : "))
    # error = bool(input("Enter tolerance value : "))
    rclpy.init(args=args)

    node = my_node()

    rclpy.spin(node)

    rclpy.shutdown()
    

if __name__ == "__main__":

    main()