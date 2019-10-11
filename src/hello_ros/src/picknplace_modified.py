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
import shape_msgs.msg as shape_msgs
from sensor_msgs.msg import JointState
import tf_conversions
import math
import tf, random
from gazebo_msgs.srv import DeleteModel, SpawnModel
from geometry_msgs.msg import Quaternion,Pose,Point
global position

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
  		group.set_goal_orientation_tolerance(0.01)
  		group.set_goal_tolerance(0.01)
  		group.set_goal_joint_tolerance(0.01)
  		group.set_goal_position_tolerance(0.01)
  		group.set_num_planning_attempts(1000)   # try 1000 times
		self.group = group
		## trajectories for RVIZ to visualize.
		self.display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path',moveit_msgs.msg.DisplayTrajectory,queue_size=1000)
		self.scene_pub = rospy.Publisher('/move_group/monitored_planning_scene', moveit_msgs.msg.PlanningScene,queue_size=1000)
		self.position = []
		self.time = 5    # regular rest time
		self.currentJointState = JointState()
		#print some basic infomation
  		print "============ Reference frame: %s" % group.get_planning_frame()    # the reference frame for this robot
  		print "============ End effector frame: %s" % group.get_end_effector_link()  	# the end-effector link for this group
  		print "============ Robot Groups:"  
  		print self.robot.get_group_names()      # groups in the robot
  		print "============ robot state"
  		print self.robot.get_current_state()    # state of the robot

  	#@staticmethod
  	'''def cube_spawn():
  		print("Waiting for gazebo services...")
    	#rospy.init_node("spawn_products_in_bins")
    	rospy.wait_for_service("gazebo/delete_model")
    	rospy.wait_for_service("gazebo/spawn_sdf_model")
    	print("Got it.")
    	delete_model = rospy.ServiceProxy("gazebo/delete_model", DeleteModel)
    	spawn_model = rospy.ServiceProxy("gazebo/spawn_sdf_model", SpawnModel)

    	with open("/home/student/catkin_ws/src/hello_ros/urdf/cube.urdf", "r") as f:
        	product_xml = f.read()

    	orient = Quaternion(*tf_conversions.transformations.quaternion_from_euler(0., 0.0, 0.785398))

    	num_of_cubes = random.randint(2,6)# generate 2-6 cubes randomly

    	for num in xrange(0,num_of_cubes):
        	bin_y   =   random.uniform(0,0.5)
        	bin_x   =   random.uniform(0,0.5)
        	item_name   =   "cube{}".format(num)
        	print("Spawning model:%s", item_name)
        	item_pose   =   Pose(Point(x=bin_x, y=bin_y, z=1),   orient) # spawn cubes randomly on the table
        	spawn_model(item_name, product_xml, "", item_pose, "world")

		# spawn the bucket
    	with open("/home/student/catkin_ws/src/hello_ros/urdf/bucket.urdf", "r") as f:
        	product_xml = f.read()

    	item_pose   =   Pose(Point(x=0.53, y=-0.23,    z=0.78),   orient) #the location of the bucket is fixed
    	print("Spawning model:%s", "bucket")
    	spawn_model("bucket", product_xml, "", item_pose, "world")
    	'''

	def call_back(self, msg):
		'''call back function for the cube position subscriber'''
		print 'Received'
		self.position = msg.pose

	def listenToGazebo(self):
		''' subscribe the position of the cubes'''
		print 'Listening...'
		rospy.Subscriber('gazebo/model_states', ModelStates, self.call_back, queue_size=1000)
		print "1212121"
		print self.position
		print "009087"
		print position

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
  		print 'Received!'
  		currentJointState.header.stamp = rospy.get_rostime()
  		tmp = 0.005     # set the finger joint variables smaller
  		#print currentJointState.position
  		#tmp_tuple=tuple([tmp] + list(currentJointState.position[1:]))
  		currentJointState.position = tuple(list(currentJointState.position[:6]) + [tmp] + [tmp]+ [tmp])
  		for i in range(1):
  			pub.publish(currentJointState)
  			print 'Published!'
    		rospy.sleep(self.time)

	def closeGripper(self):
		''' close the gripper after dropping the objects'''
    	#rospy.init_node('test_publish')
 		# Setup subscriber
  		#rospy.Subscriber("/joint_states", JointState, jointStatesCallback)
  		currentJointState = self.currentJointState
 		pub = rospy.Publisher("/jaco/joint_control", JointState, queue_size=1)
 		currentJointState = rospy.wait_for_message("/joint_states",JointState)     # get current joint variables, 9 joints here
  		print 'Received!'
  		currentJointState.header.stamp = rospy.get_rostime()
  		tmp = 0.7   # set the finger joint variables larger
  		#tmp_tuple=tuple([tmp] + list(currentJointState.position[1:]))
  		#print currentJointState.position
  		currentJointState.position = tuple(list(currentJointState.position[:6]) + [tmp] + [tmp]+ [tmp])
  		for i in range(1):
  			pub.publish(currentJointState)
  			print 'Published!'
  			rospy.sleep(self.time)

  	def rvizTraj(self, plan):
  		'''show the plan in rviz'''
  		print "==========Show in rviz"
  		display_trajectory = moveit_msgs.msg.DisplayTrajectory()
  		display_trajectory.trajectory_start = self.robot.get_current_state()
  		display_trajectory.trajectory.append(plan)
  		self.display_trajectory_publisher.publish(display_trajectory);


  	def moveJoint(self, joint_value, show_plan=False, show_rviz=False):
  		'''set joint variable values, then move the arm'''
  		group = self.group
  		# joint_value = self.robot.get_current_state().joint_state.position
		group.set_joint_value_target(joint_value)
		plan = group.plan()
		if show_plan:
			print "========== Show the plan"
			print plan
			print "=========="
		if show_rviz:
			self.rvizTraj(plan)
		#group.go(wait=True)
		group.execute(plan,wait=True)
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
			print "========== Show the plan"
			print plan
			print "=========="
		if show_rviz:
			self.rvizTraj(plan)
		#group.go(wait=True)
		group.execute(plan,wait=True)
		rospy.sleep(self.time)  # rest 5 seconds

	def moveObj(self, series, show_plan = False, show_rviz=False, height = 0.95):
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
  		#print pose_goal
  		group.set_pose_target(pose_goal)
  		plan = group.plan()
  		if show_plan:
			print "========== Show the plan"
			print plan
			print "=========="
		if show_rviz:
			self.rvizTraj(plan)
  		#group.go(wait=True)
		group.execute(plan,wait=True)
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
			print "========== Show the plan"
			print plan
			print "=========="
		if show_rviz:
			self.rvizTraj(plan)
  		#group.go(wait=True)
		group.execute(plan,wait=True)
		rospy.sleep(self.time)

	def poseCorrection(self, corr, show_plan = False, show_rviz=False):
		'''set the position deviation, then move the arm, corr:[x,y,z,x,y,z,w]'''
		group = self.group
		pose_goal = group.get_current_pose().pose
  		position = self.position
		pose_goal.position.x = pose_goal.position.x+corr[0]
  		pose_goal.position.y = pose_goal.position.y+corr[1]
  		pose_goal.position.z = pose_goal.position.z+corr[2]
  		pose_goal.orientation.x = pose_goal.orientation.x+corr[3]
  		pose_goal.orientation.y = pose_goal.orientation.y+corr[4]
  		pose_goal.orientation.z = pose_goal.orientation.z+corr[5]
  		pose_goal.orientation.w = pose_goal.orientation.w+corr[6]
  		#print pose_goal
  		group.set_pose_target(pose_goal)
  		plan = group.plan()
  		if show_plan:
			print "========== Show the plan"
			print plan
			print "=========="
		if show_rviz:
			self.rvizTraj(plan)
  		#group.go(wait=True)
		group.execute(plan,wait=True)
		rospy.sleep(self.time)

	def pickAndPlace(self,series):
		'''pick a cube and drop it into the bucket'''
		## move to the object
		print "==========cube"+str(series)+"/"+str(len(self.position)-3)
		self.moveObj(2+series)
		## close the gripper
		self.closeGripper()
		## arm up
		self.poseCorrection([0,0,0.5,0,0,0,0])
		## move to the bucket
		self.moveObj(-1,height = 1.5)
		## open the gripper
		self.openGripper()
		## return to the origin
		self.movePose([0,0,0,0,0,0])

	def moveIt(self):
		self.listenToGazebo()
		cube_num = len(self.position)-3  # the number of the cubes
		for i in range(cube_num):
			self.pickAndPlace(i)

	def test(self):
		self.listenToGazebo()
		print "***********************"
		print self.position
		self.moveObj(2)
		## close the gripper
		self.closeGripper()
		## arm up
		self.poseCorrection([0,0,0.5,0,0,0,0])
		## move to the bucket
		self.moveObj(-1,height = 1.5)
		## open the gripper
		self.openGripper()
		## return to the origin
		self.movePose([0,0,0,0,0,0])


	def run(self,is_start=False):
		try:
			if is_start:
				Planner.cube_spawn()
			#self.moveIt()
			self.test()
			R = rospy.Rate(50)
			while not rospy.is_shutdown():
				rospy.spin()
				R.sleep
		except rospy.ROSInterruptException:
			pass


if __name__=="__main__":
	p = Planner()
	#p.run(is_start=True)
	p.run()
