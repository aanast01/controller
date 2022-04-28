#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Bool
from time import sleep

start=False
dronePose = PoseStamped()

def start_cb(msg):
    global start
    start = msg.data
    
def pose_callback(pose):
    global dronePos
    dronePos = pose
	

def talker():
    global start, dronePose
    rospy.init_node('pose_pub', anonymous=True)
    rospy.Subscriber('/red/avoider/done', Bool, start_cb)
    rospy.Subscriber("/red/pose", PoseStamped, pose_callback)
    pub = rospy.Publisher('/red/tracker/input_pose', PoseStamped, queue_size=10)
    rate = rospy.Rate(10)
    while not start:
        rate.sleep() 
    if not rospy.is_shutdown():
        pose = PoseStamped()
        pose.pose.position.x    = dronePos.pose.position.x
        pose.pose.position.y    = dronePos.pose.position.y
        pose.pose.position.z    = dronePos.pose.position.z
        pose.pose.orientation.x = dronePos.pose.orientation.x
        pose.pose.orientation.y = dronePos.pose.orientation.y
        pose.pose.orientation.z = dronePos.pose.orientation.z + 1
        pose.pose.orientation.w = dronePos.pose.orientation.w + 1
        pub.publish(pose)
        sleep(3)    
        pose.pose.position.x    = dronePos.pose.position.x
        pose.pose.position.y    = dronePos.pose.position.y
        pose.pose.position.z    = dronePos.pose.position.z
        pose.pose.orientation.x = dronePos.pose.orientation.x
        pose.pose.orientation.y = dronePos.pose.orientation.y
        pose.pose.orientation.z = dronePos.pose.orientation.z - 2
        pose.pose.orientation.w = dronePos.pose.orientation.w
        pub.publish(pose)
        sleep(2)    
  
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
