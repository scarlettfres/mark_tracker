#!/usr/bin/env python
import roslib
roslib.load_manifest('detection_multi_cam')
import sys
import rospy
import cv2
import numpy as np
from std_msgs.msg import String, Header, Float32 
from sensor_msgs.msg import Image
from geometry_msgs.msg import PointStamped, Point
from visualization_msgs.msg import Marker
import tf
import time
import math as m

# !!!!! On publie nos coordonnees avec :
# rostopic pub valeur_point geometry_msgs/PointStamped '[0, now, /left_camera]' '[1.0, 2.0, 3.0]' -1
# le -1 signifie juste une fois 

mon_fichier = open("fichier.txt", "w")

def write_point(point):
	text= str(point.point.x) + " "+ str(point.point.y)+" "+ str(point.point.z)
	return text

def quaternionToEuler(x,y,z,w):
	print "coucou"
	#theta_x = m.atan2(-2)
	theta_x=m.atan2(3,2)
	theta_x=m.atan2(-2*y*z+2*x*w,1-2*x*x-2*y*y)
	theta_y=m.asin(2*x*z+2*y*w)
	theta_z=m.atan2(2*x*w+2*y*z,1-2*z*z-2-w*w)
	return theta_x,theta_y,theta_z

class result_point:

	def __init__(self):
		print "sleep ..."
  		time.sleep(30)
  		print "ok"
		rospy.Timer(rospy.Duration(10), self.timer_callback)
  		rospy.Subscriber("/cam0/visualization_marker", Marker,self.point_estimation_callback)
  		#rospy.Subscriber("/cam0/visualization_marker", Marker,self.point_estimation_callback)
  		self.listener = tf.TransformListener()

  		self.eulerX_pub = rospy.Publisher("eulerXAngle", Float32, queue_size=5)
  		self.eulerY_pub = rospy.Publisher("eulerYAngle", Float32, queue_size=5)
  		self.eulerZ_pub = rospy.Publisher("eulerZAngle", Float32, queue_size=5)
  		#rospy.Subscriber("/valeur_point", PointStamped,self.point_reel_callback)
  		self.compteur=0
		self.reel_enter=0
		self.eulerAngle=[0,0,0]
		self.towrite=""

	def timer_callback(self,data):
		
		mon_fichier.write(self.towrite)
		mon_fichier.write("\n")
		print self.towrite
		self.reel_enter+=10


	def point_estimation_callback(self,data):		
		
		#print"000000000000"
		trans,rot = self.listener.lookupTransform('/ar_marker_1', '/map', rospy.Time(0))
		#print"000000000000"
		#print trans, rot 

		#print quaternion
		euler = tf.transformations.euler_from_quaternion(rot)
		#print "tf func",euler
		vect_pose=[trans[0],trans[1],trans[2],euler[0]*180/m.pi,euler[1]*180/m.pi,euler[2]*180/m.pi]
		
		if vect_pose:
			self.towrite=str(self.reel_enter)
			for i in range(0,len(vect_pose)):
				self.towrite=self.towrite+" "+str(vect_pose[i])
			

def main(args):

	rospy.init_node('save_data', anonymous=True)
	noeud = result_point()
	try:
		rospy.spin()
	except KeyboardInterrupt:
		print "Shutting down"
		mon_fichier.close()
		print "Finished."

if __name__ == '__main__':
    main(sys.argv)

