#!/usr/bin/env python
import roslib
roslib.load_manifest('detection_multi_cam')
import sys
import rospy
import cv2
import time
import numpy as np
from std_msgs.msg import String, Header, Float32
from sensor_msgs.msg import Image
from geometry_msgs.msg import PointStamped, Point
from visualization_msgs.msg import Marker
import tf
from os import chdir

nbr_camera=2 #TODO
chdir("/home/sfress/catkin_ws/src/detection_multi_cam/launch/") # to put lauch_tf in the right folder

mon_fichier = open("launch_tf.launch", "w")


class create_tf:

	def __init__(self):

		rospy.Subscriber("/cam0/visualization_marker", Marker,self.mark0_callback)
		self.listener = tf.TransformListener()

		print"init"


	def mark0_callback(self,data):
		
		try:
			print '/camera0 /map'
			print self.listener.lookupTransform('/camera0', '/map', rospy.Time(0))
			print '/ar_marker_0 /map'
			print self.listener.lookupTransform('/ar_marker_0', '/map', rospy.Time(0))

		except Exception, e:
			print "can't read calibration files !! they should be in /src/StereoColorTracking-master/camera_info/ : ",e  
			
				
def main(args):

	rospy.init_node('raaa', anonymous=True)
	noeud = create_tf()
	try:
		rospy.spin()
	except KeyboardInterrupt:
		print "Shutting down"
		mon_fichier.close()
		print "Finished."

if __name__ == '__main__':
    main(sys.argv)





