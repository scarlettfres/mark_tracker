#!/usr/bin/env python  
import roslib
roslib.load_manifest('detection_multi_cam')
import rospy
import math
import tf
import time
import sys
from visualization_msgs.msg import Marker
from sensor_msgs.msg import JointState
from geometry_msgs.msg import Point
from tf.transformations import quaternion_from_euler, euler_from_quaternion

id_markeur_tete=2
temps_erreur=1
#sensor_msgs/JointState

mon_fichier = open("fichier_pub.txt", "w")
# ~~~~~~~variables magiques ~~~~~~~~~~~

class publish_coord:
    def __init__(self):

        self.coord_pub = rospy.Publisher("result/coord", Point, queue_size=5)
        self.angle_pub = rospy.Publisher("result/angle", Point, queue_size=5)
        rospy.Subscriber("/cam0/visualization_marker", Marker,self.mark_callback)
        rospy.Timer(rospy.Duration(0.1), self.timer_callback)
        self.listener = tf.TransformListener()
        self.broadcaster = tf.TransformBroadcaster()

        self.detection=0

        #que se passe t il si la marque disparait pendant plus d'un temps t ? un message d'erreur apparait et on arrete de publier les tf 
        self.clock_verif_erreur = rospy.Time.now() + rospy.Duration(temps_erreur)

        
    def mark_callback(self,data):
        if data.id==id_markeur_tete:
            self.clock_verif_erreur = rospy.Time.now() + rospy.Duration(temps_erreur)
            self.detection=1
        elif rospy.Time.now()> self.clock_verif_erreur:
            self.detection=0
            print "non detection de la marque ", id_markeur_tete
        
    def timer_callback(self,data):   
        if self.detection==1 :
            now = rospy.Time.now()
            rotation=(0,0,0,1)
            try:
                (trans_fin,rot_fin) = self.listener.lookupTransform( "/mon_tf/base_link", "/map", rospy.Time(0))#5
                #(trans_fin,rot_fin) = self.listener.lookupTransform(  "/map","ar_marker_3", rospy.Time(0))#5  newwwww
                euler_fin=euler_from_quaternion(rot_fin)
                #quaternion_to_tf=rot_fin
                #if euler_fin[2]>1.57:

                    #rotation=quaternion_from_euler(0,0,0)
                    #quaternion_to_tf=quaternion_from_euler(euler_fin[0],euler_fin[1],euler_fin[2])
                    #euler_fin=(euler_fin[0],euler_fin[1],euler_fin[2])


                
                #self.broadcaster.sendTransform((0,0,0),rotation,now,"/ar_markeur_sca","/ar_marker_3")#3
                #(trans_fin,rot_jojo) = self.listener.lookupTransform(  "/map","/ar_markeur_sca", rospy.Time(0))#5  newwwww
                #euler_jojo=euler_from_quaternion(rot_jojo)


                point_coord=Point()
                point_coord.x=trans_fin[0]
                point_coord.y=trans_fin[1]
                point_coord.z=trans_fin[2]

                point_angle=Point()
                point_angle.x=euler_fin[0]*180/math.pi
                point_angle.y=euler_fin[1]*180/math.pi
                point_angle.z=euler_fin[2]*180/math.pi
                
                self.coord_pub.publish(point_coord)
                self.angle_pub.publish(point_angle)
                #towrite=str(now)+" "+str(euler_fin[0])+" "+str(euler_fin[1])+" "+str(euler_fin[2])+" "+ str(euler_jojo[0])+" "+str(euler_jojo[1])+" "+str(euler_jojo[2])
               # towrite=towrite+"\n"
               # mon_fichier.write(towrite)

            except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                print "except listener " 
        
def main(args):
    rospy.init_node('publish_coord', anonymous=True)
    noeud = publish_coord()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print "Shutting down"
        mon_fichier.close()
        print "Finished."

if __name__ == '__main__':
    main(sys.argv)

