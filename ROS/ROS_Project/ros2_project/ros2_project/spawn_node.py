#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
# 1) import message/service types 
from turtlesim.srv import Kill 
from turtlesim.srv import Spawn
from turtlesim.msg import Pose
from example_interfaces.msg import Bool
import numpy as np 


class myClient(Node):
    def __init__(self):
        # node name  should be (unique)
        super().__init__("Client_node")

        # 2) send request by calling service_client with reqeust values as
        self.x = float(np.random.randint(1,11))
        self.y = float(np.random.randint(1,11))
        self.theta = float(np.random.randint(0,np.pi))
        self.spawn_client(self.x,self.y,self.theta,"Moha")
        self.pub = self.create_publisher(Pose, "position", 10)
        self.create_subscription(Bool, "flag", self.flag_callback, 10)
        self.create_timer(1/1, self.callback)


    def spawn_client(self,x,y,theta,name):
        # 4) create client object create_client(type,service_name) 
        client = self.create_client(Spawn,"spawn")

        # 5) wait for service to run 
        while client.wait_for_service(0.25)==False:
            self.get_logger().warn("wating for server")

        # 6) create a request object to fill its members
        request = Spawn.Request()
        # 7) fill request attributes/variables with values
        request.name = name 
        request.x = x
        request.y = y
        request.theta = theta

        # 8) send service request and execute callback when getting result
        futur_obj = client.call_async(request)
        futur_obj.add_done_callback(self.spawn_response_call)

    # 9) define callback with response as input
    def spawn_response_call(self,future_msg):
        self.get_logger().info("Done")
    
    def callback(self):
        # publish the pose 
        pose = Pose()
        #fill message fields 
        pose.x = self.x
        pose.y = self.y
        pose.theta = self.theta

        self.pub.publish(pose)

    # create another turtle after killing the last one 
    def flag_callback(self,data):
        if data.data:
            self.x = float(np.random.randint(1,11))
            self.y = float(np.random.randint(1,11))
            self.theta = float(np.random.randint(0,np.pi))
            self.spawn_client(self.x,self.y,self.theta,"Moha")



def main(args = None):

    rclpy.init(args=args)
    node = myClient()
    rclpy.spin(node)
    rclpy.shutdown()
    

if __name__ == "__main__":

    main()