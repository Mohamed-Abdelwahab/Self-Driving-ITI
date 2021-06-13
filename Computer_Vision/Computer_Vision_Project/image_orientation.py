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
        # subscribe to camera topic 
        self.create_subscription(Image,"/intel_realsense_d435_depth/image_raw",self.img_cb, rclpy.qos.qos_profile_sensor_data)
        
        self.get_logger().info("subscriber is started")
        self.counter = 0
        self.prev_image = 0.0
        self.f = True
    # A function to convert from rotation to Euler angels
    def rotationToVtk(self,R):
        '''
        Concert a rotation matrix into the Mayavi/Vtk rotation paramaters (pitch, roll, yaw)
        '''
        def euler_from_matrix(matrix):
            """Return Euler angles (syxz) from rotation matrix for specified axis sequence.
            :Author:
            `Christoph Gohlke <http://www.lfd.uci.edu/~gohlke/>`_

            full library with coplete set of euler triplets (combinations of  s/r x-y-z) at
                http://www.lfd.uci.edu/~gohlke/code/transformations.py.html

            Note that many Euler angle triplets can describe one matrix.
            """
            # epsilon for testing whether a number is close to zero
            _EPS = np.finfo(float).eps * 5.0

            # axis sequences for Euler angles
            _NEXT_AXIS = [1, 2, 0, 1]
            firstaxis, parity, repetition, frame = (1, 1, 0, 0) # ''

            i = firstaxis
            j = _NEXT_AXIS[i+parity]
            k = _NEXT_AXIS[i-parity+1]

            M = np.array(matrix, dtype='float', copy=False)[:3, :3]
            if repetition:
                sy = np.sqrt(M[i, j]*M[i, j] + M[i, k]*M[i, k])
                if sy > _EPS:
                    ax = np.arctan2( M[i, j],  M[i, k])
                    ay = np.arctan2( sy,       M[i, i])
                    az = np.arctan2( M[j, i], -M[k, i])
                else:
                    ax = np.arctan2(-M[j, k],  M[j, j])
                    ay = np.arctan2( sy,       M[i, i])
                    az = 0.0
            else:
                cy = np.sqrt(M[i, i]*M[i, i] + M[j, i]*M[j, i])
                if cy > _EPS:
                    ax = np.arctan2( M[k, j],  M[k, k])
                    ay = np.arctan2(-M[k, i],  cy)
                    az = np.arctan2( M[j, i],  M[i, i])
                else:
                    ax = np.arctan2(-M[j, k],  M[j, j])
                    ay = np.arctan2(-M[k, i],  cy)
                    az = 0.0

            if parity:
                ax, ay, az = -ax, -ay, -az
            if frame:
                ax, az = az, ax
            return ax, ay, az
        r_yxz = np.array(euler_from_matrix(R))*180/np.pi
        r_xyz = r_yxz[[1, 0, 2]]
        return r_xyz
    # image callback to detect and calculate orientation 
    def img_cb(self,message):

        #read first frame 
        if self.f == True :
            self.prev_image = bridge.imgmsg_to_cv2(message, "bgr8")
            self.f = False

        # recieve image from every 5 images
        if self.counter % 5 == 0 :
            
            MIN_MATCH_COUNT = 3
            # read current image
            img = bridge.imgmsg_to_cv2(message, "bgr8")
            #mask = np.zeros_like(img,np.uint8)
            #cv2.imwrite('saved_img.png', cv2_img)
            #Convert to grayscale 
            gray1 = cv2.cvtColor(self.prev_image,cv2.COLOR_BGR2GRAY)
            gray2 = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

            # step(1)

            # Initiate detector
            sift = cv2.SIFT_create()
            # find the keypoints and descriptors 
            kp1, des1 = sift.detectAndCompute(self.prev_image,None)
            kp2, des2 = sift.detectAndCompute(img,None)
            # Matching step
            FLANN_INDEX_KDTREE = 1
            index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
            search_params = dict(checks = 50)
            flann = cv2.FlannBasedMatcher(index_params, search_params)
            print(len(des1),len(des2))
            matches = flann.knnMatch(des1,des2,k=2)
            # store all the good matches as per Lowe's ratio test.
            good = []
            for m,n in matches:
                if m.distance < 0.7*n.distance:
                    good.append(m)


            # step(2)

            if len(good)>= 0:
                src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
                dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
                # Get rotation matrix M between the 2 descriptors
                M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
                matchesMask = mask.ravel().tolist()
                h,w,d = self.prev_image.shape
                pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
                dst = cv2.perspectiveTransform(pts,M)
                img = cv2.polylines(img,[np.int32(dst)],True,255,3, cv2.LINE_AA)

                # step (3)

                draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                singlePointColor = None,
                matchesMask = matchesMask, # draw only inliers
                flags = 2)
                img3 = cv2.drawMatches(self.prev_image,kp1,img,kp2,good,None,**draw_params)
                #plt.imshow(img3, 'gray'),plt.show() 
                #print(f"time = {time.time() - t0}")
                
                # Get Euler angels from rotation matrix 
                x = self.rotationToVtk(M) 
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(img3, f"yaw angel = {x[2]}", (0, 25), font, 1, (0, 0, 255), 1, cv2.LINE_AA)
                cv2.imshow("cv2_img", img3)
                #cv2.imshow("mask_img", mask)
                cv2.waitKey(1)

                self.prev_image = img
            else:
                print( "Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT) )
                matchesMask = None


        self.counter += 1
          
def main (args=None):
    rclpy.init(args=args)
    node=my_node()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__=="__main__":
    main()

