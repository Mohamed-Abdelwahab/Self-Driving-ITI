#!/usr/bin/env python3

import rclpy
import numpy as np
import math
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
# OpenCV2 for saving an image
import cv2
import time
# Instantiate CvBridge
bridge = CvBridge()

class my_node (Node):
    def __init__(self):
        super().__init__("sub_node")
        self.create_subscription(Image,"/intel_realsense_d435_depth/image_raw",self.img_cb, rclpy.qos.qos_profile_sensor_data)
        
        self.get_logger().info("subscriber is started")


        
    def img_cb(self,message):
        img = bridge.imgmsg_to_cv2(message, "bgr8")
        mask = np.zeros_like(img,np.uint8)
        #cv2.imwrite('saved_img.png', cv2_img)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        t0 = time.time()
        corners = cv2.goodFeaturesToTrack(gray,120,0.01,1)
        corners = np.int0(corners)
        for i in corners:
            x,y = i.ravel()
            cv2.circle(img,(x,y),1,255,-1)
            cv2.circle(mask,(x,y),1,255,-1)
            
        print(f"time = {time.time() - t0}")
        cv2.imshow("cv2_img", img)
        cv2.imshow("mask_img", mask)
        cv2.waitKey(1)

          
def main (args=None):
    rclpy.init(args=args)
    node=my_node()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__=="__main__":
    main()

