#!/usr/bin/env python
## Created by Group 5
## 07/10/2019
#####updated on 10/10/19 by Ruchir 
#get location of the cubes
#################################################
#Created by 
#Lin  07/10
#Ruchir 10/10
#Lei
#Yasin



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
import copy
import shape_msgs.msg as shape_msgs
from sensor_msgs.msg import JointState
import tf_conversions
import math

currentJointState = JointState()
def jointStatesCallback(msg):
  global currentJointState
  currentJointState = msg

def open():
  #rospy.init_node('test_publish')
 
  # Setup subscriber
  #rospy.Subscriber("/joint_states", JointState, jointStatesCallback)
 
  pub = rospy.Publisher("/jaco/joint_control", JointState, queue_size=1)
 
  currentJointState = rospy.wait_for_message("/joint_states",JointState)
  print 'Received!'
  currentJointState.header.stamp = rospy.get_rostime()
  tmp = 0.005
  print currentJointState.position
  #tmp_tuple=tuple([tmp] + list(currentJointState.position[1:]))
  currentJointState.position = tuple(list(currentJointState.position[:6]) + [tmp] + [tmp]+ [tmp])
  for i in range(1):
    pub.publish(currentJointState)
    print 'Published!'
    #rospy.sleep(30)

def close():
  #rospy.init_node('test_publish')
 
  # Setup subscriber
  #rospy.Subscriber("/joint_states", JointState, jointStatesCallback)
 
  pub = rospy.Publisher("/jaco/joint_control", JointState, queue_size=1)
 
  currentJointState = rospy.wait_for_message("/joint_states",JointState)
  print 'Received!'
  currentJointState.header.stamp = rospy.get_rostime()
  tmp = 0.7
  #tmp_tuple=tuple([tmp] + list(currentJointState.position[1:]))
  print currentJointState.position
  currentJointState.position = tuple(list(currentJointState.position[:6]) + [tmp] + [tmp]+ [tmp])
  for i in range(3):
    pub.publish(currentJointState)
    print 'Published!'
    rospy.sleep(5)
 
  print 'end!'



def planning():
 ## plan the path 
	moveit_commander.roscpp_initialize(sys.argv)   #initialize the moveit commander(a class), allowing us to communicate with the move_group
	rospy.init_node('move_arm',anonymous=True)     
	robot = moveit_commander.RobotCommander()

	scene = moveit_commander.PlanningSceneInterface()
	p = moveit_commander.PlanningScene()
	p.is_diff=True   # initialize the scene

	arm_group = moveit_commander.MoveGroupCommander('Arm')
	arm_group.set_planner_id("RRTkConfigDefault")
	## trajectories for RVIZ to visualize.
	display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path',moveit_msgs.msg.DisplayTrajectory,queue_size=1000)
	scene_pub = rospy.Publisher('/move_group/monitored_planning_scene', moveit_msgs.msg.PlanningScene,queue_size=1000)
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
  		 	pass
  			#scene.add_mesh('bucket', p,'./catkin_ws/src/hello_ros/urdf/bucket.dae')
  	scene_pub.publish(moveit_msgs.msg.PlanningScene)
 	## setup the planner
  	arm_group.set_goal_orientation_tolerance(0.01)
  	arm_group.set_goal_tolerance(0.01)
  	arm_group.set_goal_joint_tolerance(0.01)
  	arm_group.set_goal_position_tolerance(0.01)
  	arm_group.set_num_planning_attempts(1000)
##############################################################################
# open the gripper
  	open() #change # right position for opening of a gripper

  	#rospy.sleep(20)
  	arm_group.stop()
  	arm_group.clear_pose_targets()
	rospy.sleep(2)
  	#print "==========Start Place"
  	#joint_state = JointState()
	#joint_state.header = Header()
	#joint_state.header.stamp = rospy.Time.now()
	#joint_state.name = ['jaco_arm_0_joint', 'jaco_arm_1_joint', 'jaco_arm_2_joint', 'jaco_arm_3_joint', 'jaco_arm_4_joint', 'jaco_arm_5_joint', 'jaco_finger_joint_0', 'jaco_finger_joint_2', 'jaco_finger_joint_4']
	#joint_state.position = [0., 0., 0., 0., 0., 0., 0.05, 0.05, 0.05]
	#moveit_robot_state = moveit_msgs.msg.RobotState()
	#moveit_robot_state.joint_state = joint_state
	#arm_group.set_start_state(moveit_robot_state)
	#arm_group.set_start_state_to_current_state()
	# put the arm in the start position
	print "=========="
	joint_value = robot.get_current_state().joint_state.position
	arm_group.set_joint_value_target([0.,0.,0.,0.,0.,0.])
	plan1 = arm_group.plan()
	print "========== SHOW THE PLAN"
	print plan1
	print "=========="
	display_trajectory = moveit_msgs.msg.DisplayTrajectory()
  	display_trajectory.trajectory_start = robot.get_current_state()
  	display_trajectory.trajectory.append(plan1)
  	display_trajectory_publisher.publish(display_trajectory);
	#arm_group.go(wait=True)
	#arm_group.execute(plan1,wait=True)
	rospy.sleep(5)  # rest 5 seconds

	# arm up
	print "========== ARM UP"
	variable_values = arm_group.get_current_joint_values()
	variable_values[0] = -1.5
	variable_values[2] = -2
	#variable_values[4] = variable_values[4]-8
	#variable_values[3] = -1.5
	#variable_values[5] = -1.5
	arm_group.set_joint_value_target(variable_values)
	plan2 = arm_group.plan()
	#arm_group.go(wait=True)


######################################################################################################################################################################################
#Cube 1 Part
	# cube 1
	print "========== Cube1"
	pose_goal = arm_group.get_current_pose().pose
  	global position # position [robot,desk,cube0,cube1,cube2,...,bucket]
  	cube = position[1]
  	#pose_goal.orientation = geometry_msgs.msg.Quaternion(*tf_conversions.transformations.quaternion_from_euler(cube.orientation.x, cube.orientation.y, cube.orientation.z))
  	#pose_goal.orientation.w = cube.orientation.w
  	#pose_goal.orientation.x = cube.orientation.x
  	#pose_goal.orientation.y = cube.orientation.y  
  	#pose_goal.orientation.z = cube.orientation.z	
  	pose_goal.position.x =cube.position.x
  	pose_goal.position.y =cube.position.y
  	#pose_goal.position.z =cube.position.z
  	pose_goal.orientation = geometry_msgs.msg.Quaternion(*tf_conversions.transformations.quaternion_from_euler(0., -math.pi/2, 0.))
  	#pose_goal.position.x =0.38
  	#pose_goal.position.y =0.42
  	pose_goal.position.z = 1  #1
  	print pose_goal
  	arm_group.set_pose_target(pose_goal)
  	plan3 = arm_group.plan()
  	print "============ Visualizing plan3"
  	display_trajectory = moveit_msgs.msg.DisplayTrajectory()
  	display_trajectory.trajectory_start = robot.get_current_state()
  	display_trajectory.trajectory.append(plan3)
  	display_trajectory_publisher.publish(display_trajectory);
  	print "============ Waiting while plan3 is visualized (again)..."
  	rospy.sleep(5.)
  	#arm_group.go(wait=True)
	arm_group.execute(plan3)

################################################################################
#Write a code move it near the cube 1

	pose_goal.position.z = 0.95   #1.75 
        print pose_goal
        arm_group.set_pose_target(pose_goal)
        plan4 = arm_group.plan()
        print "============ Visualizing plan4"
#        display_trajectory = moveit_msgs.msg.DisplayTrajectory()
#        display_trajectory.trajectory_start = robot.get_current_state()
#        display_trajectory.trajectory.append(plan4)
#        display_trajectory_publisher.publish(display_trajectory);
	print "============ Waiting while plan4 is visualized (again)..."
        rospy.sleep(5.)
        arm_group.go(wait=True)
       # arm_group.execute(plan4)
 



#################################################################################
#closing of a gripper 
	close() # change  #right position of the closing of a gripper
	arm_group.stop()
	arm_group.clear_pose_targets()
	rospy.sleep(5)
################################################################################
#Select a position of the bucket 



################################################################################

###################################################################################################################################################
## test
  	print "========== GO BACK"
	arm_group.set_joint_value_target([0.,0.,0.,0.,0.,0.])
 	plan5 = arm_group.plan()
 	rospy.sleep(0.5)
 	display_trajectory = moveit_msgs.msg.DisplayTrajectory()
 	display_trajectory.trajectory_start = robot.get_current_state()
  	display_trajectory.trajectory.append(plan5)
  	display_trajectory_publisher.publish(display_trajectory);
 	rospy.sleep(0.5)
 	arm_group.go(wait=True)

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
		R = rospy.Rate(50)
		while not rospy.is_shutdown():
			R.sleep()
	except rospy.ROSInterruptException:
		pass

