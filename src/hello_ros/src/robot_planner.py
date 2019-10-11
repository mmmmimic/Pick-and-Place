#!/usr/bin/env python
'''
mini project1
pick and place
Created by Group 5
07/10/2019
'''

import roslib
roslib.load_manifest('hello_ros')

import rospy
import numpy as np
from std_msgs.msg import String
from gazebo_msgs.msg import ModelStates
import sys
import moveit_commander
import geometry_msgs.msg
import moveit_msgs.msg
import copy
from sensor_msgs.msg import JointState
import tf_conversions
import math
import tf, random
import sys
#pos = []

class Planner(object):
	'''Pick and Place Robot'''
	def __init__(self, *args, **kwargs):
		'''Initialization'''
		print "Initializing the program"
		moveit_commander.roscpp_initialize(sys.argv)   #initialize the moveit commander(a class), allowing us to communicate with the move_group
		rospy.init_node('move_arm',anonymous=True)    # initialize the node, note that there is only allowed to be one node in a program 
		self.robot = moveit_commander.RobotCommander()
		self.scene = moveit_commander.PlanningSceneInterface()
		p = moveit_commander.PlanningScene()
		p.is_diff=True   # initialize the scene
		group = moveit_commander.MoveGroupCommander('Arm')   # move the arm
		group.set_planner_id("RRTkConfigDefault")   # the default planner is RTT
		## setup the planner
		self.update()
  		group.set_goal_orientation_tolerance(0.01)
  		group.set_goal_tolerance(0.01)
  		group.set_goal_joint_tolerance(0.05)
  		group.set_goal_position_tolerance(0.01)
  		group.set_num_planning_attempts(100)   # try 100 times
		self.group = group
		## trajectories for RVIZ to visualize.
		self.display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path',moveit_msgs.msg.DisplayTrajectory,queue_size=1000)
		self.scene_pub = rospy.Publisher('/move_group/monitored_planning_scene', moveit_msgs.msg.PlanningScene,queue_size=1000)
		self.time = 1  # regular rest time
		self.currentJointState = JointState()
		#print some basic infomation
  		print "============ Reference frame: %s ============" % group.get_planning_frame()    # the reference frame for this robot
  		print "============ End effector frame: %s ============" % group.get_end_effector_link()  	# the end-effector link for this group
  		print "============ Robot Groups:"  
  		print self.robot.get_group_names()      # groups in the robot
  		print "============ robot state"
  		print self.robot.get_current_state()    # state of the robot
		print "============"

	def createScene(self):
		'''Create the scene and import the objects into the rviz'''
		position = self.position
		po_size = len(position) # the number of elements of the objects in the "world"
  		cube_num = po_size-3    # the number of cubes is equal to the sum minus 'robot' and 'desk'
  		for i in range(cube_num+1):   # put the objects
  		 	p = geometry_msgs.msg.PoseStamped()   # data type: stamped
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
  		 		print "cube"+str(i)+" added!"
  		 	else:
  				#scene.add_mesh('bucket', p,'./catkin_ws/src/hello_ros/urdf/bucket.dae')  # try to import bucket into the scene but failed //2019.10.8
  				print "bucket added!"
  		self.scene_pub.publish(moveit_msgs.msg.PlanningScene)     # publish the scene

  	def openGripper(self):
  		''' open the gripper to fetch objects'''
  		#rospy.init_node('test_publish')
  		# Setup subscriber
  		#rospy.Subscriber("/joint_states", JointState, jointStatesCallback)
  		currentJointState = self.currentJointState 
 		pub = rospy.Publisher("/jaco/joint_control", JointState, queue_size=1)
 		currentJointState = rospy.wait_for_message("/joint_states",JointState)  # get current joint variables, 9 joints here
  		#print 'Received!'
  		currentJointState.header.stamp = rospy.get_rostime()
  		tmp = 0.005     # set the finger joint variables smaller
  		#print currentJointState.position
  		#tmp_tuple=tuple([tmp] + list(currentJointState.position[1:]))
  		currentJointState.position = tuple(list(currentJointState.position[:6]) + [tmp] + [tmp]+ [tmp])
  		for i in range(3):
  			pub.publish(currentJointState)
  			#print 'Published!'
			rospy.sleep(self.time)

	def closeGripper(self):
		''' close the gripper after dropping the objects'''
    	#rospy.init_node('test_publish')
 		# Setup subscriber
  		#rospy.Subscriber("/joint_states", JointState, jointStatesCallback)
  		currentJointState = self.currentJointState
 		pub = rospy.Publisher("/jaco/joint_control", JointState, queue_size=1)
 		currentJointState = rospy.wait_for_message("/joint_states",JointState)     # get current joint variables, 9 joints here
  		#print 'Received!'
  		currentJointState.header.stamp = rospy.get_rostime()
  		tmp = 0.7   # set the finger joint variables larger
  		#tmp_tuple=tuple([tmp] + list(currentJointState.position[1:]))
  		#print currentJointState.position
  		currentJointState.position = tuple(list(currentJointState.position[:6]) + [tmp] + [tmp]+ [tmp])
  		for i in range(3):
  			pub.publish(currentJointState)
  			#print 'Published!'
			rospy.sleep(self.time)

  	def rvizTraj(self, plan):
  		'''show the plan in rviz'''
  		print "============Show in rviz============"
  		display_trajectory = moveit_msgs.msg.DisplayTrajectory()
  		display_trajectory.trajectory_start = self.robot.get_current_state()
  		display_trajectory.trajectory.append(plan)
  		self.display_trajectory_publisher.publish(display_trajectory);

	def showPlan(self, plan):
    		'''show the plan'''
		print "============ Show the plan ============"
		print plan
		print "============"

  	def moveJoint(self, joint_value, show_plan=False, show_rviz=False):
  		'''set joint variable values, then move the arm'''
  		group = self.group
  		# joint_value = self.robot.get_current_state().joint_state.position
		group.set_joint_value_target(joint_value)
		plan = group.plan()
		if show_plan:
			self.showPlan()
		if show_rviz:
			self.rvizTraj(plan)
		#group.go(wait=True)
		group.execute(plan,wait=True)
		group.stop()
		rospy.sleep(self.time) # rest 5 seconds

	def jointCorrection(self, deviation, show_plan=False, show_rviz=False):
		'''set the joint variable deviation, then move the arm'''
		group = self.group
  		joint_value = self.robot.get_current_state().joint_state.position
  		#print joint_value
  		#print deviation
  		joint_value = list(joint_value)
  		for i in range(6):
  			joint_value[i] = joint_value[i]+deviation[i]
  		#joint_value = tuple(joint_value)
  		#print joint_value[:6]
		group.set_joint_value_target(joint_value[:6])
		plan = group.plan()
		if show_plan:
			self.showPlan()
		if show_rviz:
			self.rvizTraj(plan)
		#group.go(wait=True)
		group.execute(plan,wait=True)
		group.stop()
		rospy.sleep(self.time)  # rest 5 seconds

	def moveObj(self, series, show_plan = False, show_rviz=False, height = 1):
		'''move the end effector to on the top of an object'''
		group = self.group
		pose_goal = group.get_current_pose().pose
  		position = self.position
  		objects = position[series]   # position[robot,desk,cube0,cube1,...,bucket]
  		pose_goal.position.x =objects.position.x
  		pose_goal.position.y =objects.position.y
  		#pose_goal.position.z =cube.position.z
  		pose_goal.orientation = geometry_msgs.msg.Quaternion(*tf_conversions.transformations.quaternion_from_euler(0., -math.pi/2, 0.))  # make the gripper normal to the desk
  		pose_goal.position.z =height  # 0.95 is the best value we can have, but we can change the height
  		#print series
		#print pose_goal
  		group.set_pose_target(pose_goal)
  		plan = group.plan()
  		if show_plan:
			self.showPlan()
		if show_rviz:
			self.rvizTraj(plan)
  		group.go(wait=True)
		#group.execute(plan,wait=True)
		group.stop()
		rospy.sleep(self.time)

	def movePose(self, pose, show_plan = False, show_rviz=False, is_rot = False):
		'''move the end effector to a given position, pose:[x,y,z,r,p,y]'''
		group = self.group
		pose_goal = group.get_current_pose().pose
  		position = self.position
  		if is_rot:
  			pose_goal.orientation = geometry_msgs.msg.Quaternion(*tf_conversions.transformations.quaternion_from_euler(0., -math.pi/2, 0.))  # make the gripper normal to the desk
  		else:
  			pose_goal.orientation = geometry_msgs.msg.Quaternion(*tf_conversions.transformations.quaternion_from_euler(pose[3], pose[4], pose[5]))  # make the gripper normal to the desk
  		pose_goal.position.x = pose[0]
  		pose_goal.position.y = pose[1]
  		pose_goal.position.z = pose[2]
  		#print pose_goal
  		group.set_pose_target(pose_goal)
  		plan = group.plan()
  		if show_plan:
			self.showPlan()
		if show_rviz:
			self.rvizTraj(plan)
  		#group.go(wait=True)
		group.execute(plan,wait=True)
		group.stop()
		rospy.sleep(self.time)

	def poseCorrection(self, pos, ang=[0.,-math.pi/2,0.], show_plan = False, show_rviz=False):
		'''set the position deviation, then move the arm, pos:[x,y,z] ang:[r,p,y]'''
		group = self.group
		pose_goal = group.get_current_pose().pose
  		position = self.position
		pose_goal.position.x = pose_goal.position.x+pos[0]
  		pose_goal.position.y = pose_goal.position.y+pos[1]
  		pose_goal.position.z = pose_goal.position.z+pos[2]
		pose_goal.orientation = geometry_msgs.msg.Quaternion(*tf_conversions.transformations.quaternion_from_euler(ang[0], ang[1], ang[2]))
  		print pose_goal
  		group.set_pose_target(pose_goal)
  		plan = group.plan()
  		if show_plan:
			self.showPlan()
		if show_rviz:
			self.rvizTraj(plan)
  		#group.go(wait=True)
		group.execute(plan,wait=True)
		group.stop()
		#rospy.sleep(self.time)

	def update(self):
    		'''update the place of the cubes'''
		print "-> update position"
		State = rospy.wait_for_message("/gazebo/model_states", ModelStates)  # get cube positions
		self.position = State.pose

	def pickAndPlace(self,series):
		'''pick a cube and drop it into the bucket'''
		print "move to the object"
		print "----------cube"+str(series+1)+"/"+str(len(self.position)-3)+"----------"
		print "-> above the cube"
		self.moveObj(2+series)   # moveObj(2) is to move the first cube
		#print "-> open the gripper"
		#self.openGripper()
		print "-> go down"
		self.moveObj(2+series,height=0.94)
		print "-> close the gripper"
		self.closeGripper()
		print "-> rise up"
		self.moveObj(2+series, height=1.25)
		print "-> move to the bucket"
		self.moveObj(-1,height = 1.45)
		print "-> open the gripper"
		self.openGripper()
		print ' '

	def run(self):
		try:
			cube_num = len(self.position)-3  # the number of the cubes
			#print "initializing... -> open the gripper"
			#self.openGripper()
			for i in range(cube_num):
				self.pickAndPlace(i)
				self.update() # update the cube place to avoid accidental collisions
			R = rospy.Rate(50)
			while not rospy.is_shutdown():
				rospy.spin()
				R.sleep
		except rospy.ROSInterruptException:
			pass


if __name__=="__main__":
	#global pos
	'''def call_back(msg):
   		#print 'Received'
   		global pos
   		pos = msg.pose # record the position of the robots,cubes and bucket
   		print pos
	#rospy.Subscriber('gazebo/model_states', ModelStates, call_back, queue_size=1000)
	#print pos
	#sys.exit(1)
	'''
	p = Planner()
	p.run()
