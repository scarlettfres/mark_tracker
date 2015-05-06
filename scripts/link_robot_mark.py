#!/usr/bin/env python  
import roslib
roslib.load_manifest('mark_tracker')
import rospy
import tf
import time
import sys
from visualization_msgs.msg import Marker
from sensor_msgs.msg import JointState
from os import chdir

# ~~~~~~~variables magiques ~~~~~~~~~~~

ID_markeur=2
markeur="ar_marker_"+str(ID_markeur)
robot_body_part="/HeadTouchFront_frame"
robot_ref="/base_link"
robot_foot="/base_footprint"
dist_x=-2.05
dist_y=0.48
temps_erreur=1  #sec 
chdir("/home/sfress/catkin_ws/src/mark_tracker/launch/") # to put lauch_tf in the right folder
mon_fichier = open("launch_link_robot_mark.launch", "w")

# ~~~~~~~variables magiques ~~~~~~~~~~~

class link_head_robot:
    def __init__(self):

        rospy.Subscriber("/joint_states", JointState ,self.joint_state_callback)    # pour caler la clock
        rospy.Subscriber("/cam0/visualization_marker", Marker,self.mark_callback)
        self.listener = tf.TransformListener()
        self.broadcaster = tf.TransformBroadcaster()
        self.detection=0
        self.trans_markeur_to_body=(0,0,0)
        self.rot_markeur_to_body=(0,0,0,1)
        
        #que se passe t il si la marque disparait pendant plus d'un temps t ? un message d'erreur apparait et on arrete de publier les tf 
        self.clock_verif_erreur = rospy.Time.now() + rospy.Duration(temps_erreur)


    def write_launch(self):
        #ecrite d'un fichier .launch dans lequel les coord de 
        #la cam vont etes enregistrees de maniere a ce que notre marque se trouve ne 0 

            message=str("""<launch>
    <node pkg="tf" type="static_transform_publisher" 
        name="link_robot_mark" args=" """)
        
            message = message+ str(self.trans_markeur_to_body[0])+" "+str(self.trans_markeur_to_body[1])+" "+str(self.trans_markeur_to_body[2])+" "    # transaltion puis rotation (attention pas le meme ordre dangles)
            message = message+str(self.rot_markeur_to_body[0])+" "+str(self.rot_markeur_to_body[1])+" "+str(self.rot_markeur_to_body[2])
            message = message+" "+str(self.rot_markeur_to_body[3])+" " +markeur+" /mon_tf"+robot_body_part +str(""" 30"/>
</launch>""")
           
            print "======message saved in launchfile : "
            print message
            print "======"
            mon_fichier.write(message)
            rospy.signal_shutdown('init file written ! You can now launch "detection_post_calib" node ')
            
    def mark_callback(self,data):
        if data.id==ID_markeur:
            self.clock_verif_erreur = rospy.Time.now() + rospy.Duration(temps_erreur)
            self.detection=1
        elif rospy.Time.now()> self.clock_verif_erreur:
            self.detection=0
            print "non detection de la marque ", id_markeur_tete
 
    def joint_state_callback(self,data):   
        if self.detection==1 :
            now = rospy.Time.now()
            try:
                
                (trans_body_to_ref,rot_body_to_ref) = self.listener.lookupTransform(robot_body_part, robot_ref, rospy.Time(0))
                #(trans_body_to_ref,rot_body_to_ref) = self.listener.lookupTransform("/HeadTouchFront_frame", "/base_link", rospy.Time(0))
                (trans_foot_to_body,rot_foot_to_body) = self.listener.lookupTransform(robot_foot, robot_body_part, rospy.Time(0))
                (trans_markeur_to_map,rot_markeur_to_map) = self.listener.lookupTransform(markeur, "map", rospy.Time(0))

                #permet de prendre en compte l'inclinaison de la marque par rapport a son positionnement sur la tete => depart avec base robot sur map
                # jusqua present on ne sait pas ou se situe le robot dans notre referentiel, pour cela on publie des donnees de la ou devrait etre notre robot
                # dans le referentiel de la map

                #les pieds du robot doivent etre ici par rapport a la map  
                self.broadcaster.sendTransform((dist_x,dist_y,0),(0,0,0,1),now,"/mon_tf/base_footprint","/map") 
                # donc notre body part serait ici par rapport a la map
                self.broadcaster.sendTransform(trans_foot_to_body,rot_foot_to_body,now,"/mon_tf/"+robot_body_part,"/mon_tf/base_footprint")
                #on a donc maintenant notre body_part et notre mark qui appartiennent au meme arbre : on peut connaitre la transformation qui les separe
                (self.trans_markeur_to_body,self.rot_markeur_to_body) = self.listener.lookupTransform(markeur, "/mon_tf/"+robot_body_part, rospy.Time(0))
                self.broadcaster.sendTransform(self.trans_markeur_to_body,self.rot_markeur_to_body,now,"/rololo", markeur) 

                self.write_launch()
            except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                print " waiting for tf..."
        
def main(args):
    rospy.init_node('link_head_robot', anonymous=True)
    noeud = link_head_robot()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print "Shutting down"
        mon_fichier.close()
        print "Finished."

if __name__ == '__main__':
    main(sys.argv)