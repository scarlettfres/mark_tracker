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
precision=0.02
depart_taton=0.2
erreur=0.02
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
        self.init_trans_position_baselink=(0,0,0)
        self.init_rot_mark=(0,0,0,1)

        self.position_x=0
        self.position_y=0
        self.dist_mark_tete=0
        self.detection=0

        self.old_x=0
        self.old_y=0

        #que se passe t il si la marque disparait pendant plus d'un temps t ? un message d'erreur apparait et on arrete de publier les tf 
        self.clock_verif_erreur = rospy.Time.now() + rospy.Duration(temps_erreur)
        self.clock_save_old_x = rospy.Time.now() 

        
    def mark_callback(self,data):
    	# tant qu'il voit une marque, il repousse le temps de verif d'une seconde, sinon, le temps finit par depasser le temps de verif
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
                (trans_map,rot_map) = self.listener.lookupTransform(markeur,  "map",rospy.Time(0))
                #print trans_map,rot_map
                #permet de prendre en compte l'inclinaison de la marque par rapport a son positionnement sur la tete => depart avec base robot sur map
                if self.flag==0:
                    print "ok"
                    (_,self.init_rot_mark) = self.listener.lookupTransform(markeur,"map", rospy.Time(0))
                    (t_map,_) = self.listener.lookupTransform("map",markeur, rospy.Time(0))
                    (t_hauteur,r_hauteur) = self.listener.lookupTransform(head,"base_footprint", rospy.Time(0))
                    self.dist_mark_tete= t_map[2] + t_hauteur[2]
                    self.flag=1
                    print self.dist_mark_tete

                self.broadcaster.sendTransform((self.position_x, self.position_y,-self.dist_mark_tete),self.init_rot_mark,now,"/mon_tf/head",markeur)

                self.broadcaster.sendTransform(trans,rot,now,"/mon_tf/base_link","/mon_tf/head")
                (trans_fin,rot_fin) = self.listener.lookupTransform( "/mon_tf/base_link", "/map", rospy.Time(0))
                self.broadcaster.sendTransform(trans_fin,rot_fin,now, "/map","/base_link")

                ecartx=abs(trans_fin[0]-self.old_x)
                ecarty=abs(trans_fin[1]-self.old_y)

                result=1
                compteur=0
                OK_X=0
                OK_Y=0
                it=depart_taton
                #print ecartx,ecarty
                #ici pour placer bien comme il faut le marquer sur la tete 
                if ecartx > erreur or ecarty > erreur:
	                print "111"
	                while OK_X==1 and OK_Y==1:
	                	print " while "
						print "pas assez precis"
						if OK_X==0:
							self.position_x=self.position_x+it*result
							#self.position_y=self.position_y+0.001*result
							self.broadcaster.sendTransform((self.position_x, self.position_y,-self.dist_mark_tete),self.init_rot_mark,now,"/mon_tf/head",markeur)
							self.broadcaster.sendTransform(trans,rot,now,"/mon_tf/base_link","/mon_tf/head")
							(trans_fin,rot_fin) = self.listener.lookupTransform( "/mon_tf/base_link", "/map", rospy.Time(0))
							self.broadcaster.sendTransform(trans_fin,rot_fin,now, "/map","/base_link")

							if abs(trans_fin[0]-self.old_x)>ecartx or abs(trans_fin[1]-self.old_y):
								if result == -1: # si literation precedente on avait deja change de sens 
									compteur += 1
								result=-1
								
							else:	# ie on a diminue lerreur
								result = 1
								
							if compteur ==2:
								it=it/2

							if it < 0.001:
								OK_X=1
								result=1
								compteur=0
								it=depart_taton
								print self.position_x

							ecartx=abs(trans_fin[0]-self.old_x)
							ecarty=abs(trans_fin[1]-self.old_y)

						if OK_X==1:
							#self.position_x=self.position_x+it*result
							self.position_y=self.position_y+it*result
							self.broadcaster.sendTransform((self.position_x, self.position_y,-self.dist_mark_tete),self.init_rot_mark,now,"/mon_tf/head",markeur)
							self.broadcaster.sendTransform(trans,rot,now,"/mon_tf/base_link","/mon_tf/head")
							(trans_fin,rot_fin) = self.listener.lookupTransform( "/mon_tf/base_link", "/map", rospy.Time(0))
							self.broadcaster.sendTransform(trans_fin,rot_fin,now, "/map","/base_link")
							if abs(trans_fin[0]-self.old_x)>ecartx or abs(trans_fin[1]-self.old_y):
								if result == -1: # si literation precedente on avait deja change de sens 
									compteur += 1
								result=-1
								
							else:	# ie on a diminue lerreur
								result = 1
								
							if compteur ==2:
								it=it/2

							if it < 0.001:
								OK_Y=1
								print self.position_x

							ecartx=abs(trans_fin[0]-self.old_x)
							ecarty=abs(trans_fin[1]-self.old_y)
                #else:
                    # print "ok"
                if now>self.clock_save_old_x:
                	print"mag tps"
                	self.old_x=trans_fin[0]
                	self.old_y=trans_fin[1]
                	self.clock_save_old_x = rospy.Time.now() + rospy.Duration(2)




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

