#!/usr/bin/env python

import rospy

from dynamic_reconfigure.server import Server
from detection_multi_cam.cfg import firstConfig

def callback(config, level):
    rospy.loginfo("""Reconfigure Request: {x}, {y},\ 
          {z}, {Roll}, {Pitch}, {Yaw}""".format(**config))
    return config

if __name__ == "__main__":
    rospy.init_node("marker_parameters")

    srv = Server(firstConfig, callback)
    rospy.spin()
