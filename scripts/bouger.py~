#!/usr/bin/env python
import roslib
import rospy
import naoqi
import time
roslib.load_manifest('detection_multi_cam')
import numpy as np

from visualization_msgs.msg import Marker
from std_msgs.msg import Empty
from std_msgs.msg import String

from geometry_msgs.msg import Twist # for sending commands to the drone
from naoqi import ALProxy

VITESSE=0.1
#IP="127.0.0.1"
IP="10.0.206.111"
PORT=9559
class bouger:
	

	def __init__(self):
		self.init()

	
		
		
	def init(self):
		rospy.init_node('bouger', anonymous=True)
		self.motionProxy = ALProxy("ALMotion",IP,PORT)
		#self.postureProxy = ALProxy("ALRobotPosture", IP,PORT)
		rospy.Timer(rospy.Duration(1), self.timer_callback)
		rospy.spin()
		
	def timer_callback(self,data):
		
			Head = self.motionProxy.getPosition('Head',0, True)
			self.motionProxy.moveTo(x, y, theta)
			#PositionRight = self.motionProxy.getPosition('RForeArm',0, True)
			print Head
		
			
				
				#self.motionProxy.setPosition ("LArm", 0, vectl, VITESSE, 7)
			
				
				#self.motionProxy.setPosition ("RArm", 0,vectr, VITESSE, 7)
			
		
		

if __name__ == '__main__':
    bouger()
