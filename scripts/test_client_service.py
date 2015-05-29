#!/usr/bin/env python

import sys
import rospy
import mark_tracker_tools.srv


if __name__ == "__main__":
    rospy.wait_for_service('init_plan')
    try:
        init_plan = rospy.ServiceProxy('add_two_ints', AddTwoInts)
        resp = init_plan(2, "axis")
    return resp1.sum
    except rospy.ServiceException, e:
    print "Service call failed: %s"%e