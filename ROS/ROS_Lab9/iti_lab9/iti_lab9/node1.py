#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
#  import message/service types 
from turtlesim.srv import Spawn
from turtlesim.msg import Pose
from std_srvs.srv import Empty
from geometry_msgs.msg import Twist

f = open("turtle_commands.csv",'r')
v = []
for line in f:
        
    v.append(line[:-1].split(','))

class myClient(Node):
    def __init__(self):
        # node name  should be (unique)
        super().__init__("Client_node")

        self.current_x = 0.0
        self.current_y = 0.0
        self.current_angel = 0.0
        self.linear_velocity = 0.0
        self.angular_velocity = 0.0
        #create counter
        self.i = 1
        #  create subscriber to know current (x,y)
        self.create_subscription(Pose, "turtle1/pose", self.pose_callback, 10)
        # create publisher 
        self.pub = self.create_publisher(Twist,"/turtle1/cmd_vel",10)
        self.create_timer(1/1,self.callback)
        
        
    def callback(self):

        if self.i > 12 :
            self.i = 1

        # create message object
        msg = Twist()
        # fill data in message 
        msg.linear.x = float(v[self.i][0])
        msg.linear.y = 0.0
        msg.linear.z = 0.0
        msg.angular.x = 0.0
        msg.angular.y = 0.0
        msg.angular.z = float(v[self.i][1])

        self.pub.publish(msg)
        self.i += 1

    # create sub callback 
    def pose_callback(self,pose):

        # update robot state 
        self.current_x = pose.x
        self.current_y = pose.y  
        self.current_angel = pose.theta
        self.linear_velocity = pose.linear_velocity
        self.angular_velocity = pose.angular_velocity

        
        # check if the robot exceed the boundries of (x,y)
        if (2 > self.current_x or self.current_x > 8 ) or (2 > self.current_y or self.current_y > 8 ):
            # self.get_logger().info(f"x : { self.current_x}\n")
            # self.get_logger().info(f"y : { self.current_y}\n")

            # create client object 
            client = self.create_client(Empty,"reset")

        # 5) wait for service to run 
            # while client.wait_for_service():
            #     self.get_logger().warn("wating for server")
       
            # create request object 
            request = Empty.Request()
            # send request 
            futur_obj = client.call_async(request)
            # call reset callback when recieving response 
            futur_obj.add_done_callback(self.reset_response_call)
    
    def reset_response_call(self,future_msg):
        self.get_logger().info("Done")



def main(args = None):

    rclpy.init(args=args)
    node = myClient()
    rclpy.spin(node)
    rclpy.shutdown()
    

if __name__ == "__main__":

    main()

