#!/usr/bin/env python
import roslib
roslib.load_manifest('mark_tracker')
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


nbr_camera = 1  # TODO
# chdir("/home/sfress/catkin_ws/src/mark_tracker/launch/") # to put
# lauch_tf in the right folder

mon_fichier = open("launch_tf_cam_map.launch", "w")


class create_tf:

    def __init__(self, launch_path, camera_name):

        rospy.Subscriber(
            "/cam0/visualization_marker", Marker, self.mark0_callback)

        chdir(launch_path)
        self.mon_fichier = open("launch_tf_cam_map.launch", "w")
        self.camera_name = camera_name

        self.marker_pub = rospy.Publisher("marqueur_rviz", Marker)

        self.listener = tf.TransformListener()

        self.br = tf.TransformBroadcaster()

        print"init"

        #rospy.Subscriber("/valeur_point", PointStamped,self.point_reel_callback)
        # TODO = mettre ce qui suit en param !
        # self.nbr_camera=rospy.get_param("nbr_camera")
        # self.name_file=rospy.get_param("name_file")
        self.nbr_camera = 2
        self.compteur = 0
        self.numero_cam = 0
        self.input = -1
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

    def write_launch(self, data, euler, num):
        # ecrite d'un fichier .launch dans lequel les coord de
        # la cam vont etes enregistrees de maniere a ce que notre marque se
        # trouve ne 0
        message = ""
        if num == 0:
            message = "<launch>"

        message = message + str("""
	<node pkg="tf" type="static_transform_publisher"
		name="camera_axis" args=" """)

        # 0.175462652377 0.085071202854 2.94358463649 1.53053258111
        # -0.178616594811 -3.0794539535 /camera /map 30
        message = message + str(data.pose.position.x) + " " + str(data.pose.position.y) + " " + str(
            data.pose.position.z) + " "  # transaltion puis rotation (attention pas le meme ordre dangles)
        message = message + str(euler[2]) + " " + str(euler[1]) + " " + str(euler[0]) + " /map " + str(self.camera_name) + str(""" 30"/>
""")
        if num == nbr_camera - 1:
            message = message + "</launch>"
        print "======message saved in launchfile : "
        print message
        print "======"
        self.mon_fichier.write(message)
        rospy.signal_shutdown(
            'init file written ! You can now launch "detection_post_calib" node ')

    def mark0_callback(self, data):
        # si je n'ai pas encore enregistre la position de cam0
        if self.numero_cam == 0:
            if self.input != -1:
                try:
                    marqueur = '/ar_marker_' + str(self.input)
                    trans, rot = self.listener.lookupTransform(
                        marqueur, '/map', rospy.Time(0))
                except Exception, e:
                    message_error = "can't read the position of the mark! : is the mark number" + \
                        str(self.input) + "visible on the camera ?"
                    rospy.logwarn(
                        "can't read the position of the mark! : is the mark number %s visible on the camera ?", self.input)
                    print e

                quaternion = (rot)
                data.pose.position.x = trans[0]
                data.pose.position.y = trans[1]
                data.pose.position.z = trans[2]
                # print quaternion
                euler = tf.transformations.euler_from_quaternion(quaternion)
                self.compteur += 1
                if self.compteur == 10:
                    self.write_launch(data, euler, 0)
                    self.numero_cam += 1
                    self.compteur = 0
            else:
                self.input = input(
                    "put the number of your calibration mark: \n")


def updateArgs(arg_defaults):
    '''Look up parameters starting in the driver's private parameter space, but
    also searching outer namespaces.  '''
    args = {}
    for name, val in arg_defaults.iteritems():
        full_name = rospy.search_param(name)
        if full_name is None:
            args[name] = val
        else:
            args[name] = rospy.get_param(full_name, val)

    return(args)


def main(args):

    s = rospy.init_node('create_tf', anonymous=True)
    print "1", args[0]
    print "2", args[1]
    print "3", args[2]
    arg_defaults = {
        'launch_path': "/home/sfress/catkin_ws/src/mark_tracker/launch/",
        'camera_name': "/axis_camera"
    }
    # args=updateArgs(arg_defaults)
    # print args, "aaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    noeud = create_tf(args[1], args[2])
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print "Shutting down"
        self.mon_fichier.close()
        print "Finished."

if __name__ == '__main__':
    main(sys.argv)
