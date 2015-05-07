#!/usr/bin/env python  
import roslib
roslib.load_manifest('mark_tracker')
import rospy
import math
import tf
import time
import sys
from visualization_msgs.msg import Marker
from sensor_msgs.msg import JointState
from tf.transformations import quaternion_from_euler, euler_from_quaternion


# ~~~~~~~variables magiques ~~~~~~~~~~~


id_markeur_tete=2
temps_erreur=1  #sec 
markeur="ar_marker_"+str(id_markeur_tete)
robot_body_part="/HeadTouchFront_frame"


# ~~~~~~~variables magiques ~~~~~~~~~~~

class link_head_robot:
    def __init__(self,body_part,id_mark):
        self.robot_body_part=body_part
        self.id_markeur_tete=int(id_mark)
        self.markeur="ar_marker_"+str(id_mark)
        self.listener = tf.TransformListener()
        self.broadcaster = tf.TransformBroadcaster()
        self.detection=0

        print type(self.robot_body_part),type(self.id_markeur_tete),type(self.markeur)






        #que se passe t il si la marque disparait pendant plus d'un temps t ? un message d'erreur apparait et on arrete de publier les tf 
        self.clock_verif_erreur = rospy.Time.now() + rospy.Duration(temps_erreur)
        rospy.Subscriber("/joint_states", JointState ,self.joint_state_callback)
        rospy.Subscriber("/cam0/visualization_marker", Marker,self.mark_callback)
        
    def mark_callback(self,data):
        if data.id==self.id_markeur_tete:
            self.clock_verif_erreur = rospy.Time.now() + rospy.Duration(temps_erreur)
            self.detection=1
        elif rospy.Time.now()> self.clock_verif_erreur:
            self.detection=0
            print "non detection de la marque ", self.id_markeur_tete
        
    def joint_state_callback(self,data):   
        if self.detection==1 :
            now = rospy.Time.now()
            try:
                # comment est le frame sur lequel la mark est fixee par rapport a la base?
                (trans,rot) = self.listener.lookupTransform(self.robot_body_part,"base_link", rospy.Time(0))
                # ou devrait donc etre notre base_link par rapport a notre mark: on cree un base_link "virtuel"
                self.broadcaster.sendTransform(trans,rot,now,"/mon_tf/base_link","/mon_tf"+self.robot_body_part)
                # comment est notre base_link virtuel apr rapport a notre map? 
                (trans_fin,rot_fin) = self.listener.lookupTransform( "/mon_tf/base_link", "/map", rospy.Time(0))  
                if trans_fin[2]<1 :     # on continue d'envoyer l'ancienne position connue si bug inclinaison mark
                    #self.old_t=trans_fin
                    #self.old_r=rot_fin
                    #self.broadcaster.sendTransform(trans_fin,rot_fin,now, "/map","/base_link")
                    print "OK"
                else:
                    print "BUG INCLINAISON MARK"
                self.broadcaster.sendTransform(trans_fin,rot_fin,now, "/map","/base_link")
            except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                print "wait for tf ... " 



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
    rospy.init_node('link_head_mark', anonymous=True)
    arg_defaults = {
        'body_part': "/HeadTouchFront_frame",
        'id_mark':'2'
    }
    args = updateArgs(arg_defaults)
    print args
    noeud = link_head_robot(**args)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print "Shutting down"
        mon_fichier.close()
        print "Finished."

if __name__ == '__main__':
    main(sys.argv)











