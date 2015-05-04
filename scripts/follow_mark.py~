#!/usr/bin/env python
import roslib
roslib.load_manifest('detection_multi_cam')
import sys
import rospy
import cv2
import time
import numpy as np
import math as m
from std_msgs.msg import String, Header, Float32
from sensor_msgs.msg import Image
from geometry_msgs.msg import PointStamped, Point
from visualization_msgs.msg import Marker
import tf
from os import chdir
from axis_camera.msg import Axis

chdir("/home/sfress/catkin_ws/src/detection_multi_cam/launch/") # to put lauch_tf in the right folder

class follow_mark:

	def __init__(self):

		rospy.Subscriber("/state", Axis,self.state_callback)
		rospy.Subscriber("/cam0/visualization_marker", Marker,self.mark_callback)
		
		self.pub = rospy.Publisher('cmd', Axis, queue_size=5)
		self.cam=Axis()
		self.cam.pan=0
		self.cam.tilt=-85
		self.flag=0
		self.listener = tf.TransformListener()
		self.br = tf.TransformBroadcaster() # publish tf 


	def mark_callback(self,data):
		print "mark_callback"
		if self.flag==0:
			if data.pose.position.x > 0.5:
				print "iiiiiiiiiif"
				self.cam.pan += 3
				if self.cam.pan > 177:
					 self.cam.pan = 177

			if data.pose.position.x < -0.5:
				print "iiiiiiiiiif"
				self.cam.pan += -3
				if self.cam.pan <- 177:
					 self.cam.pan = -177

			if data.pose.position.y > 0.5:
				print "iiiiiiiiiif"
				self.cam.tilt += 3
				if self.cam.tilt > 0:
					 self.cam.tilt = 0

			if data.pose.position.y < -0.5:
				print "iiiiiiiiiif"
				self.cam.tilt += -3
				if self.cam.tilt < -90:
					 self.cam.tilt = -90
			#self.flag=1

			self.pub.publish(self.cam)
			print "position x=", data.pose.position.x
			print "publish= ", self.cam
			time.sleep(1)



		#if abs(data.pose.position.x)>0.3 and self.cam.pan>-177 and self.cam.pan<177 :	# attention aux signes 
			#print " netree ds le if"
			#self.cam.pan+=1*np.sign(-data.pose.position.x)
		#if abs(data.pose.position.y)>0.5 and self.cam.tilt<-3 and self.cam.tilt>-87:
			#self.cam.tilt+=1*np.sign(data.pose.position.y)



	def state_callback(self,data):
		print "staaaaate"
		self.cam.pan=data.pan
		self.cam.tilt=data.tilt


				
def main(args):

	rospy.init_node('follow_mark', anonymous=True)
	noeud = follow_mark()
	try:
		rospy.spin()
	except KeyboardInterrupt:
		print "Shutting down"
		
if __name__ == '__main__':
    main(sys.argv)





