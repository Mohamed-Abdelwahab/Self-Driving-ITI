#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
#  import message/service types 
import rclpy
import numpy as np
from rclpy.node import Node
from sensor_msgs.msg import Imu
from functions import quaternion_from_euler,euler_from_quaternion

f = open("imu_data.csv",'r')
v = []
for line in f:
        
    v.append(line[:-1].split(','))

class myNode(Node):
    def __init__(self):
        # node name  should be (unique)
        super().__init__("node2")

        #create counter
        self.i = 0
    
        # create publisher 
        self.pub = self.create_publisher(Imu,"zed2_imu",rclpy.qos.qos_profile_sensor_data)
        self.create_timer(1/30,self.callback)
        
        
    def callback(self):

        if self.i > 347 :
            self.i = 0

        # create message object
        imu_msg = Imu()
        # convert to quaternion
        Quaternion = quaternion_from_euler(self, 0.0, 0.0, np.deg2rad(float(v[self.i][6])))

        # check z angular velocity 
        if float(v[self.i][5]) > .3 :
            ang_z_vel_cov = .1
            ang_z_cov = .1
        else:
            ang_z_vel_cov = .001
            ang_z_cov = .001

        # fill message data
        imu_msg.header.frame_id= "zed2_imu_link"
        imu_msg.header.stamp= self.get_clock().now().to_msg()
        # orientation
        imu_msg.orientation.w = Quaternion.w
        imu_msg.orientation.x = Quaternion.x
        imu_msg.orientation.y = Quaternion.y
        imu_msg.orientation.z = Quaternion.z
        imu_msg.orientation_covariance = [0.01, 0.0, 0.0, 0.0, 0.01, 0.0, 0.0, 0.0, ang_z_cov]
        # angular velocity
        imu_msg.angular_velocity.x = float(v[self.i][3])
        imu_msg.angular_velocity.y = float(v[self.i][4])
        imu_msg.angular_velocity.z = float(v[self.i][5])
        imu_msg.angular_velocity_covariance=[0.01, 0.0, 0.0, 0.0, 0.01, 0.0, 0.0, 0.0, ang_z_vel_cov]
        # linear acceleration
        imu_msg.linear_acceleration.x = float(v[self.i][0])*9.81
        imu_msg.linear_acceleration.y = float(v[self.i][1])*9.81
        imu_msg.linear_acceleration.z = float(v[self.i][2])*9.81
        imu_msg.linear_acceleration_covariance=[0.01, 0.0, 0.0, 0.0, 0.01, 0.0, 0.0, 0.0, 0.01]



        self.pub.publish(imu_msg)
        self.i += 1
  


def main(args = None):

    rclpy.init(args=args)
    node = myNode()
    rclpy.spin(node)
    rclpy.shutdown()
    

if __name__ == "__main__":

    main()
    
