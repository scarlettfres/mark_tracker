#!/usr/bin/env python
import roslib
roslib.load_manifest('detection_multi_cam')
import sys
import rospy
import cv2
import time
import numpy as np
import math
from std_msgs.msg import String, Header, Float32
from sensor_msgs.msg import Image
from geometry_msgs.msg import PointStamped, Point 
from cv_bridge import CvBridge, CvBridgeError

from os import chdir
# import IPython

chdir("/home/sfress/catkin_ws/src/detection_multi_cam") # to put lauch_tf in the right folder
class take_photo:

  def __init__(self):
    
    self.bridge = CvBridge()
    print " sleep...."
    time.sleep(30)
    self.image_sub = rospy.Subscriber("/frame_reduced_out",Image,self.im_callback)
    self.clock=rospy.Time.now() + rospy.Duration(2)
    self.nbr=0



     
  def im_callback(self,data):


    now=rospy.Time.now()
    
    print now 

    if now >= self.clock:
      try:
        get = self.bridge.imgmsg_to_cv2(data, "bgr8")
        cv_image = get.copy()
      except CvBridgeError, e:
        print e
    
      #chessboard_dim = (9, 6)
      #found_all, corners = cv2.cv.FindChessboardCorners(cv_image, chessboard_dim )
      #print found_all
      print "=======>SAVIIIING<=========="
      self.nbr += 1
      titre ="imagenes/axis"+str(self.nbr)+".ppm"
      print "                     !!",   self.nbr    ,"!!              "
      cv2.imwrite(titre,cv_image)
      self.clock=rospy.Time.now() + rospy.Duration(2)




def main(args):
  rospy.init_node('take_photo', anonymous=True)

  ic = take_photo()
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print "Shutting down"
  cv2.destroyAllWindows()
  print "Finished."

if __name__ == '__main__':
    main(sys.argv)