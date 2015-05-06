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

#head='/HeadTouchFront_frame'
mon_fichier = open("fichier.txt", "w")
id_markeur_tete=2
temps_erreur=1  #sec 
markeur="ar_marker_"+str(id_markeur_tete)
#head='/HeadTouchMiddle_frame'
#head='/HeadTouchRear_frame'
head='/HeadTouchFront_frame'
#head='/Head'
dist_mark_head=0
# ou se trouve le robot lorqu'on lance ce pg? 
dist_x=-2.05
dist_y=0.48
footprint_init_=0.05
#sensor_msgs/JointState

# ~~~~~~~variables magiques ~~~~~~~~~~~

class link_head_robot:
    def __init__(self):

        rospy.Subscriber("/joint_states", JointState ,self.joint_state_callback)
        rospy.Subscriber("/cam0/visualization_marker", Marker,self.mark_callback)
        self.listener = tf.TransformListener()
        self.broadcaster = tf.TransformBroadcaster()
        # le {flag, init_trans,init_rot} permet de prendre en compte l'inclinaison de la marque par rapport a son positionnement sur la tete,
        # mais si dispositif=fixe, penser a lajouer dans un launch
        self.flag=0
        self.detection=0
        self.foot_map_t=(0,0,0)
        self.foot_map_r=(0,0,0,1)
        self.pos=(0,0,0)
        self.old_t=(0,0,0)
        self.old_r=(0,0,0,1)

        #que se passe t il si la marque disparait pendant plus d'un temps t ? un message d'erreur apparait et on arrete de publier les tf 
        self.clock_verif_erreur = rospy.Time.now() + rospy.Duration(temps_erreur)
        
    def mark_callback(self,data):
        if data.id==id_markeur_tete:
            self.clock_verif_erreur = rospy.Time.now() + rospy.Duration(temps_erreur)
            self.detection=1
        elif rospy.Time.now()> self.clock_verif_erreur:
            self.detection=0
            print "non detection de la marque ", id_markeur_tete


        
    def joint_state_callback(self,data):   
        if self.detection==1 :
            now = rospy.Time.now()
            try:
               
                (trans,rot) = self.listener.lookupTransform(head,"base_link", rospy.Time(0))
                (transtest,rottest) = self.listener.lookupTransform("base_footprint",head, rospy.Time(0))
                (trans_map,rot_map) = self.listener.lookupTransform(markeur,  "map",rospy.Time(0))
                #print trans_map,rot_map
                #permet de prendre en compte l'inclinaison de la marque par rapport a son positionnement sur la tete => depart avec base robot sur map
                
               
                if self.flag==0:
                    (t_map,r_map) = self.listener.lookupTransform(markeur,"map", rospy.Time(0))
                    (t_map_bis,r_map_bis) = self.listener.lookupTransform("map",markeur, rospy.Time(0))
                    (t_hauteur,r_hauteur) = self.listener.lookupTransform(head,"base_footprint", rospy.Time(0))
                    self.broadcaster.sendTransform((0,0,0),(0,0,0,1),now,"/mon_tf/head",markeur)#3
                    self.broadcaster.sendTransform(trans,rot,now,"/mon_tf/base_link","/mon_tf/head")#4
                    (trans_fin,rot_fin) = self.listener.lookupTransform( "/mon_tf/base_link", "/map", rospy.Time(0))#5

                    self.broadcaster.sendTransform((dist_x,dist_y,0),(0,0,0,1),now,"/mon_tf/base_footprint","/map")#aaaaaaaaaaaaaaa
                    self.broadcaster.sendTransform(transtest,rottest,now,"/mon_tf/myhead","/mon_tf/base_footprint")#aaaaaaaaaaaaaaa

                    self.broadcaster.sendTransform(trans_fin,rot_fin,now, "/map","/base_link")
                    #_,self.foot_map_r= self.listener.lookupTransform("base_footprint","/mon_tf/base_footprint", rospy.Time(0))

                    self.foot_map_t,self.foot_map_r= self.listener.lookupTransform("/mon_tf/head","/mon_tf/myhead", rospy.Time(0))
                    
                    self.flag=1



                  



                (t_map,r_map) = self.listener.lookupTransform(markeur,"map", rospy.Time(0))
                (t_map_bis,r_map_bis) = self.listener.lookupTransform("map",markeur, rospy.Time(0))

                #print "r_map ", euler_from_quaternion(r_map)
                #print "rmap_bis ", euler_from_quaternion(r_map_bis)
                #print self.init_rot_mark
                #eul=euler_from_quaternion(self.init_rot_mark)
                #print "AAAAAAAAAAAAAAAAAAA",euler_from_quaternion((-0.0057895, -0.026662, 0.00029598, 0.99963))
                #q = quaternion_from_euler(0,eul[1],eul[2])

                #eul=euler_from_quaternion(self.foot_map_r)
                #print "AAAAAAAAAAAAAAAAAAA",euler_from_quaternion((-0.0057895, -0.026662, 0.00029598, 0.99963))
                #q = quaternion_from_euler(eul[0],eul[1],eul[2])
                #self.broadcaster.sendTransform((0,0,0),(0,0,0,1),now,"/mon_tf/head",markeur)
                #print self.init_rot_mark

                self.broadcaster.sendTransform(self.foot_map_t,self.foot_map_r,now,"/mon_tf/head",markeur)
                
                
                #self.listener.lookupTransform( "base_footprint", "map", rospy.Time(0)) #5
                self.broadcaster.sendTransform(trans,rot,now,"/mon_tf/base_link","/mon_tf/head")#4
                (trans_fin,rot_fin) = self.listener.lookupTransform( "/mon_tf/base_link", "/map", rospy.Time(0))#5

                (verif_bug_t,verif_bug_r) = self.listener.lookupTransform("/map","/base_footprint", rospy.Time(0))#5


                angle_verif= euler_from_quaternion(verif_bug_r)

                if verif_bug_t[2]<0.5 :     # on continue d'envoyer l'ancienne position connue si bug inclinaison mark
                    self.old_t=trans_fin
                    self.old_r=rot_fin
                    #self.broadcaster.sendTransform(trans_fin,rot_fin,now, "/map","/base_link")
                    print "OK"
                else:
                    print "BUG INCLINAISON MARK"



                self.broadcaster.sendTransform(trans_fin,rot_fin,now, "/map","/base_link")
        
                #q = quaternion_from_euler(0,0,1.57)
                euler_fin=euler_from_quaternion(rot_fin)
                euler_map=euler_from_quaternion(rot_map)
                euler_simple=euler_from_quaternion(rot)
                towrite=str(now)+" "+str(trans_fin[0])+" "+str(trans_fin[1])+" "+str(trans_fin[2])+" "+str(euler_fin[0])+" "+str(euler_fin[1])+" "+str(euler_fin[2])+" "+str(trans[0])+" "+str(trans[1])+" "+str(trans[2])+" "+str(euler_simple[0])+" "+str(euler_simple[1])+" "+str(euler_simple[2])+" "+str(trans_map[0])+" "+str(trans_map[1])+" "+str(trans_map[2])+" "+str(euler_map[0])+" "+str(euler_map[1])+" "+str(euler_map[2])
                towrite=towrite+"\n"
                mon_fichier.write(towrite)



            except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                print "except listener " 

        
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

