#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 11:20:21 2022

@author: guilhem_galand
"""

import rospy, actionlib, tf
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from actionlib_msgs.msg import GoalStatus
from geometry_msgs.msg import Pose, Point, Quaternion
from math import pi
from time import sleep

Coordonnees = []
Coordonnees.append([-0.5,-4.5,pi])
Coordonnees.append([-2,-4.3,pi/2])
Coordonnees.append([-3,-4.2,0])
Coordonnees.append([-2,-4.3,3*pi/2])

Fonctionnement = True
Patrouille = True
Cible = 0
cibleAtteinte = False

def goto(x, y, theta, timeout=120):
    global cibleAtteinte
    cibleAtteinte = False
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = 'map'
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose = Pose(Point(x, y, 0), Quaternion(*tf.transformations.quaternion_from_euler(0, 0, theta)))
    move_base.send_goal(goal)
    rospy.loginfo("Going to x={} y={} theta={}...".format(x, y, theta))
    if move_base.wait_for_result(rospy.Duration(timeout)) and move_base.get_state() == GoalStatus.SUCCEEDED:
        rospy.loginfo("The target is reached")
        cibleAtteinte = True
    else:
        rospy.logwarn("We could NOT reach the target after " + str(timeout) + "secs")
        move_base.cancel_goal()

def Main():
    print("Going to target n°",Cible)
    goto(Coordonnees[Cible][0],Coordonnees[Cible][1],Coordonnees[Cible][2])

# Now, start the navigation node
rospy.init_node('navigation')
move_base = actionlib.SimpleActionClient("/move_base", MoveBaseAction)
rospy.loginfo("Waiting for the connection to /move_base...")
move_base.wait_for_server(rospy.Duration(20))
    
while(Fonctionnement and not rospy.is_shutdown()):
    Main()
    sleep(2)
    Cible += 1
    if Cible >= len(Coordonnees):
        Cible = 0