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


robot_ref="/base_link"
robot_foot="/base_footprint"

temps_erreur=1  #sec 


# ~~~~~~~variables magiques ~~~~~~~~~~~


class link_head_robot:
    def __init__(self,body_part,id_mark,x,y,path):

	chdir(path) # to put lauch_tf in the right folder
	self.mon_fichier = open("launch_link_robot_mark.launch", "w")
        self.robot_body_part=body_part
        self.ID_markeur=int(id_mark)
        self.markeur="ar_marker_"+str(id_mark)
        self.dist_x=float(x)
        self.dist_y=float(y)
    
        
        self.listener = tf.TransformListener()
        self.broadcaster = tf.TransformBroadcaster()
        self.detection=0
        self.trans_markeur_to_body=(0,0,0)
        self.rot_markeur_to_body=(0,0,0,1)
        
        #que se passe t il si la marque disparait pendant plus d'un temps t ? un message d'erreur apparait et on arrete de publier les tf 
        self.clock_verif_erreur = rospy.Time.now() + rospy.Duration(temps_erreur)
        rospy.Subscriber("/joint_states", JointState ,self.joint_state_callback)    # pour caler la clock
        rospy.Subscriber("/cam0/visualization_marker", Marker,self.mark_callback)


    def write_launch(self):
        #ecrite d'un fichier .launch dans lequel les coord de 
        #la cam vont etes enregistrees de maniere a ce que notre marque se trouve ne 0 

            message=str("""<launch>
    <node pkg="tf" type="static_transform_publisher" 
        name="link_robot_mark" args=" """)
        
            message = message+ str(self.trans_markeur_to_body[0])+" "+str(self.trans_markeur_to_body[1])+" "+str(self.trans_markeur_to_body[2])+" "    # transaltion puis rotation (attention pas le meme ordre dangles)
            message = message+str(self.rot_markeur_to_body[0])+" "+str(self.rot_markeur_to_body[1])+" "+str(self.rot_markeur_to_body[2])
            message = message+" "+str(self.rot_markeur_to_body[3])+" " +self.markeur+" /mon_tf"+self.robot_body_part +str(""" 30"/>
</launch>""")
           
            print "======message saved in launchfile : "
            print message
            print "======"
            self.mon_fichier.write(message)
            rospy.signal_shutdown('init file written ! You can now launch "detection_post_calib" node ')
            
    def mark_callback(self,data):
        if data.id==self.ID_markeur:
            self.clock_verif_erreur = rospy.Time.now() + rospy.Duration(temps_erreur)
            self.detection=1
        elif rospy.Time.now()> self.clock_verif_erreur:
            self.detection=0
            print "can't find the mark with the ID :  ", self.ID_markeur
 
    def joint_state_callback(self,data):   
        if self.detection==1 :
            now = rospy.Time.now()
            try:
                
                (trans_body_to_ref,rot_body_to_ref) = self.listener.lookupTransform(self.robot_body_part, robot_ref, rospy.Time(0))
                #(trans_body_to_ref,rot_body_to_ref) = self.listener.lookupTransform("/HeadTouchFront_frame", "/base_link", rospy.Time(0))
                (trans_foot_to_body,rot_foot_to_body) = self.listener.lookupTransform(robot_foot, self.robot_body_part, rospy.Time(0))
                (trans_markeur_to_map,rot_markeur_to_map) = self.listener.lookupTransform(self.markeur, "map", rospy.Time(0))

                #permet de prendre en compte l'inclinaison de la marque par rapport a son positionnement sur la tete => depart avec base robot sur map
                # jusqua present on ne sait pas ou se situe le robot dans notre referentiel, pour cela on publie des donnees de la ou devrait etre notre robot
                # dans le referentiel de la map

                #les pieds du robot doivent etre ici par rapport a la map  
                self.broadcaster.sendTransform((self.dist_x,self.dist_y,0),(0,0,0,1),now,"/mon_tf/base_footprint","/map") 
                # donc notre body part serait ici par rapport a la map
                self.broadcaster.sendTransform(trans_foot_to_body,rot_foot_to_body,now,"/mon_tf/"+self.robot_body_part,"/mon_tf/base_footprint")
                #on a donc maintenant notre body_part et notre mark qui appartiennent au meme arbre : on peut connaitre la transformation qui les separe
                (self.trans_markeur_to_body,self.rot_markeur_to_body) = self.listener.lookupTransform(self.markeur, "/mon_tf/"+self.robot_body_part, rospy.Time(0))
                self.broadcaster.sendTransform(self.trans_markeur_to_body,self.rot_markeur_to_body,now,"/rololo", self.markeur) 

                self.write_launch()
            except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                print " waiting for tf..."
  



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
    rospy.init_node('link_mark_robot', anonymous=True)
    path=str(args[0].split("scripts")[0])+"launch"
    arg_defaults = {
        'body_part': "/HeadTouchFront_frame",
        'id_mark':'2',
        'x':'-2',
        'y':'0.5'
    }

    args = updateArgs(arg_defaults)
    args['path']=path
    print args
    noeud = link_head_robot(**args)

    try:
        rospy.spin()
    except KeyboardInterrupt:
        print "Shutting down"
        self.mon_fichier.close()
        print "Finished."

if __name__ == '__main__':
    main(sys.argv)
