#!/usr/bin/env python

from service_mark_tracker.srv import *
import rospy

def sign(x):
    if x > 0:
        return 1
    if x == 0:
        return 0
    return -1

class move_pepper:
	def __init__(self):
		self.motionProxy = ALProxy("ALMotion",IP,PORT)
		self.listener = tf.TransformListener()
		self.broadcaster = tf.TransformBroadcaster()

		rospy.Subscriber("/result_position", Odometry,self.position_callback)	# useless... 
		rospy.Timer(rospy.Duration(TIMER_ALMOTION), self.timer_callback)	# useless ????
		rospy.Subscriber("/cam0/visualization_marker", Marker,self.mark_callback)
		rospy.Service('add_two_ints', AddTwoInts, self.handle_add_two_ints)

	def move_to():
		print " coucou" 

	def handle_add_two_ints(req):
	    print "Returning [%s + %s = %s]"%(req.a, req.b, (req.a + req.b))
	    return AddTwoIntsResponse(req.a + req.b)

	"""

	def handle_add_two_ints(req):
	    print "Returning [%s + %s = %s]"%(req.a, req.b, (req.a + req.b))
	    return AddTwoIntsResponse(req.a + req.b)

	def add_two_ints_server():
	    rospy.init_node('mark_server')
	    s = rospy.Service('add_two_ints', AddTwoInts, handle_add_two_ints)
	    print "Ready to add two ints."
	    rospy.spin()

	"""

if __name__ == "__main__":
	rospy.init_node('move_pepper', anonymous=True)
	class_move_pepper=move_pepper()


	try:
		rospy.spin()
	except KeyboardInterrupt:
		print "Shutting down"
		
		print "Finished."

