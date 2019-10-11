#!/usr/bin/env python
## Created by Group 5
## 07/10/2019
#####
#get location of the cubes
import roslib
roslib.load_manifest('hello_ros')
import rospy
import numpy as np
from std_msgs.msg import String
from gazebo_msgs.msg import ModelStates
#####
# grasping
import sys
import moveit_commander
import geometry_msgs.msg
global position
import moveit_msgs.msg

def planning():
 ## plan the path 
	moveit_commander.roscpp_initialize(sys.argv)   #initialize the moveit commander(a class), allowing us to communicate with the move_group
	rospy.init_node('move_arm',anonymous=True)     
	robot = moveit_commander.RobotCommander()
	scene = moveit_commander.PlanningSceneInterface()
	arm_group = moveit_commander.MoveGroupCommander('Arm')
	## trajectories for RVIZ to visualize.
	display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path',moveit_msgs.msg.DisplayTrajectory,queue_size=1000)
  	print "============ Starting tutorial "
  	## the reference frame for this robot
  	print "============ Reference frame: %s" % arm_group.get_planning_frame()
  	## the end-effector link for this group
  	print "============ End effector frame: %s" % arm_group.get_end_effector_link()
  	## groups in the robot
  	print "============ Robot Groups:"
  	print robot.get_group_names()
  	## state of the robot
  	print "============ robot state"
  	print robot.get_current_state()

  	## Create the scene
  	global position
  	po_size = len(position) # the number of elements of the objects in the "world"
  	cube_num = po_size-3
  	for i in range(cube_num+1):
  		 p = geometry_msgs.msg.PoseStamped()
 		 p.header.frame_id = robot.get_planning_frame()
 		 cube = position[i+2]
 		 p.pose.orientation.w = cube.orientation.w
 		 p.pose.orientation.x = cube.orientation.x
 		 p.pose.orientation.y = cube.orientation.y
 		 p.pose.orientation.z = cube.orientation.z
 		 p.pose.position.x = cube.position.x
 		 p.pose.position.y = cube.position.y
  		 p.pose.position.z = cube.position.z
  		 if i < cube_num:
  		 	scene.add_box('cube'+str(i), p,(0.05,0.05,0.05))
  		 else:
  		 	print p
  			scene.add_mesh('bucket', p,'./catkin_ws/src/hello_ros/urdf/bucket.dae',(1,1,1))


 	## setup the planner
  	arm_group.set_goal_orientation_tolerance(0.01)
  	arm_group.set_goal_tolerance(0.01)
  	arm_group.set_goal_joint_tolerance(0.01)
  	arm_group.set_num_planning_attempts(1000)
	# put the arm in the start position
	print "========== MOVEING TO THE START"
	arm_group.set_joint_value_target([0,0,0,0,0,0])
	plan1 = arm_group.go(wait=True)
	#rospy.sleep(5)  # rest 5 seconds

	# arm up
	print "========== ARM UP"
	arm_group.set_joint_value_target([-0.5,-0.5,0,1.5,0,0])
	plan2 = arm_group.go(wait=True)

	# cube 1
	print "========== Cube1"
	pose_goal = arm_group.get_current_pose().pose
  	#pose_goal.orientation = geometry_msgs.msg.Quaternion(*tf_conversions.transformations.quaternion_from_euler(0., -math.pi/2, 0.))
  	global position # position [robot,desk,cube0,cube1,cube2,...,bucket]
  	cube = position[2]
  	pose_goal.orientation.w = cube.orientation.w
  	pose_goal.orientation.x = cube.orientation.x
  	pose_goal.orientation.y = cube.orientation.y  
  	pose_goal.orientation.z = cube.orientation.z	
  	pose_goal.position.x =cube.position.x
  	pose_goal.position.y =cube.position.y
  	pose_goal.position.z =cube.position.z
  	#pose_goal.orientation.w = 0.92
  	#pose_goal.orientation.x = 0
  	#pose_goal.orientation.y = 0 
  	#pose_goal.orientation.z = 0.38	
  	#pose_goal.position.x =0.05
  	#pose_goal.position.y =0.33
  	#pose_goal.position.z =0.75
  	print pose_goal
  	arm_group.set_pose_target(pose_goal)
  	plan3 = arm_group.plan()
  	arm_group.go(wait=True)
  	pose_goal.position.z = 0.175
  	arm_group.set_pose_target(pose_goal)
  	plan4 = arm_group.go(wait=True)
  	moveit_commander.roscpp_shutdown()


if __name__=="__main__":
	try:
		#listen to the gazebo for the position of the cubes
		def call_back(msg):
   			#rospy.loginfo(msg.pose) # print the initial known position
   			global position
   			position = msg.pose # record the position of the robots,cubes and bucket
   		#Initialize publisher
		rospy.Subscriber('gazebo/model_states', ModelStates, call_back, queue_size=1000)
		# Initialize node
		#rospy.init_node('gazebo_listener',anonymous=True)
		planning()
		R = rospy.Rate(10)
		while not rospy.is_shutdown():
			R.sleep()
	except rospy.ROSInterruptException:
		pass

