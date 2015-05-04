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



nbr_camera=1 #TODO
chdir("/home/sfress/catkin_ws/src/detection_multi_cam/launch/") # to put lauch_tf in the right folder

mon_fichier = open("launch_tf.launch", "w")


class create_tf:

	def __init__(self):

		rospy.Subscriber("/cam0/visualization_marker", Marker,self.mark0_callback)
		
		self.marker_pub = rospy.Publisher("marqueur_rviz", Marker)

		self.listener = tf.TransformListener()

		self.br = tf.TransformBroadcaster()

		print"init"

   		#rospy.Subscriber("/valeur_point", PointStamped,self.point_reel_callback)
  		#TODO = mettre ce qui suit en param ! 
  		#self.nbr_camera=rospy.get_param("nbr_camera")
  		#self.name_file=rospy.get_param("name_file")
  		self.nbr_camera=2
		self.compteur =0
		self.numero_cam=0
		self.input=-1
		self.tf_enter = []
		self.rot_enter = []
		self.sens_enter = []
		
		self.marker = Marker()
		self.marker.header.frame_id = "/map"
		self.marker.type = self.marker.ARROW
		self.marker.action = self.marker.ADD
		self.marker.scale.x = 0.5
		self.marker.scale.y = 0.2
		self.marker.scale.z = 0.2
		self.marker.color.a = 1.0
			


	def write_launch(self,data,euler,num):
		#ecrite d'un fichier .launch dans lequel les coord de 
		#la cam vont etes enregistrees de maniere a ce que notre marque se trouve ne 0 
			message=""
			if num == 0:
				message="<launch>"

			message=message + str("""
	<node pkg="tf" type="static_transform_publisher" 
		name="camera_axis" args=" """)
		
		#0.175462652377 0.085071202854 2.94358463649 1.53053258111 -0.178616594811 -3.0794539535 /camera /map 30
			message = message+ str(data.pose.position.x)+" "+str(data.pose.position.y)+" "+str(data.pose.position.z)+" "	# transaltion puis rotation (attention pas le meme ordre dangles)
			message = message+str(euler[2])+" "+str(euler[1])+" "+str(euler[0])+" /map /axis_camera" +str(""" 30"/>
""")
			if num == nbr_camera-1:
				message=message + "</launch>"
			print "======message saved in launchfile : "
			print message
			print "======"
			mon_fichier.write(message)



	def mark0_callback(self,data):
		print " coucou"
		if self.numero_cam==0: # si je n'ai pas encore enregistre la position de cam0
			if self.input==0:
				try:
					trans,rot = self.listener.lookupTransform('/ar_marker_1', '/map', rospy.Time(0))
				except Exception, e:
					print "can't read calibration files !! they should be in /src/StereoColorTracking-master/camera_info/ : ",e  


				quaternion=(rot)
				data.pose.position.x=trans[0]
				data.pose.position.y=trans[1]
				data.pose.position.z=trans[2]
				#print quaternion
				euler = tf.transformations.euler_from_quaternion(quaternion)
				self.compteur += 1
				if self.compteur == 10:
					self.write_launch(data,euler,0)
					self.numero_cam += 1
					self.compteur = 0
			else:
				self.input = input("put 0 to calibrate first cam: \n")

	

				
def main(args):

	rospy.init_node('create_tf', anonymous=True)
	noeud = create_tf()
	try:
		rospy.spin()
	except KeyboardInterrupt:
		print "Shutting down"
		mon_fichier.close()
		print "Finished."

if __name__ == '__main__':
    main(sys.argv)





