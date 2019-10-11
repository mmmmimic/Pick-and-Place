# !/usr/bin/env python
# This program publishes randomly-generated velocity
# Messages for turtlesim.
import rospy
import sys
import copy
import tf_conversions
import shape_msgs.msg as shape_msgs
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
import math
# we import the model_states msgs in order to use them
from gazebo_msgs.msg import ModelStates
from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list
from sensor_msgs.msg import JointState
from numpy import zeros, array, linspace


currentJointState = JointState()
def jointStatesCallback(msg):
  global currentJointState
  currentJointState = msg

def open():
    currentJointState = rospy.wait_for_message("/joint_states",JointState)
    currentJointState.header.stamp = rospy.get_rostime()
    tmp = 0.005
    currentJointState.position = tuple(list(currentJointState.position[:6]) + [tmp] + [tmp]+ [tmp])
    rate=rospy.Rate(10)
    for i in range(3):
        pub_open.publish(currentJointState)
        rate.sleep()
    print'The gripper has opened.'
    
def close():
    currentJointState = rospy.wait_for_message("/joint_states",JointState)
    currentJointState.header.stamp = rospy.get_rostime()
    tmp = 0.7
    currentJointState.position = tuple(list(currentJointState.position[:6]) + [tmp] + [tmp]+ [tmp])
    rate=rospy.Rate(10)
    for i in range(3):
        pub_close.publish(currentJointState)
        rate.sleep()
    print 'The gripper has closed'

# Initialization
moveit_commander.roscpp_initialize(sys.argv)
pub_close=rospy.Publisher('/jaco/joint_control',JointState,queue_size=1)
pub_open=rospy.Publisher('/jaco/joint_control',JointState,queue_size=1)
rospy.init_node('move_the_cubes',anonymous=True)
robot=moveit_commander.RobotCommander()
scene=moveit_commander.PlanningSceneInterface()
group=moveit_commander.MoveGroupCommander("Arm")

# Setup the planner
group.set_goal_orientation_tolerance(0.01)
group.set_goal_tolerance(0.01)
group.set_goal_joint_tolerance(0.05)
group.set_num_planning_attempts(100)

#Get the position of the cubes
models=rospy.wait_for_message('/gazebo/model_states',ModelStates)
poses=models.pose
model_num=len(poses)
print'Now we have'+str(model_num)+' objects.'

#Get the position of cube 0

cube_num=model_num-3;
for i in range(cube_num):
    '''
    i=0;

    if (i+1)<=model_num:
        print('/n')
    else:
        print('bad index')
    '''
    #To get the postion of cube
    start_index=2+i;
    ort=poses[start_index].orientation
    pst=poses[start_index].position
    print'orientation'
    print(pst)
    print'position'
    print(ort)

    #To get the position of bucket
    bucket_pose=poses[model_num-1]
    bpst=bucket_pose.position

    ##1. step2 move to the cube
    # Bring the arm to the location of the object, minus a certain amount of space
    print'First, move to the above of the cube'
    pose_goal = group.get_current_pose().pose
    pose_goal.orientation=geometry_msgs.msg.Quaternion(*tf_conversions.transformations.quaternion_from_euler(0,-math.pi/2, 0))
    pose_goal.position.x=pst.x
    pose_goal.position.y=pst.y
    pose_goal.position.z=1
    group.set_pose_target(pose_goal)
    plan1=group.plan()
    group.go(wait=True)
    group.stop()
    #2. step2 Open the gripper
    print'Second, open the gripper'
    open()
    rospy.sleep(1)

    #3. step3 keep moving downard
    print'Third, Move_down and approach the cube'
    pose_goal = group.get_current_pose().pose
    pose_goal.orientation=geometry_msgs.msg.Quaternion(*tf_conversions.transformations.quaternion_from_euler(0, -math.pi/2, 0))
    pose_goal.position.x=pst.x
    pose_goal.position.y=pst.y
    pose_goal.position.z=0.95
    group.set_pose_target(pose_goal)
    plan2=group.plan()
    group.go(wait=True)
    group.stop()
    rospy.sleep(1)

    #4. close the gripper
    print'Close the fucking gripper'
    close()
    rospy.sleep(3)
    #5. rise arm
    print'Raise arm now to another position'
    pose_goal = group.get_current_pose().pose
    pose_goal.orientation=geometry_msgs.msg.Quaternion(*tf_conversions.transformations.quaternion_from_euler(0, -math.pi/2, 0))
    pose_goal.position.x=pst.x
    pose_goal.position.y=pst.y
    pose_goal.position.z=1.25
    group.set_pose_target(pose_goal)
    plan2=group.plan()
    group.go(wait=True)
    group.stop()
    rospy.sleep(1)


    #6. Move to the bucket
    print 'Move to the bucket'
    pose_goal = group.get_current_pose().pose
    pose_goal.orientation=geometry_msgs.msg.Quaternion(*tf_conversions.transformations.quaternion_from_euler(0, -math.pi/2, 0))
    pose_goal.position.x=bpst.x
    pose_goal.position.y=bpst.y
    pose_goal.position.z=1.45
    group.set_pose_target(pose_goal)
    plan3=group.plan()
    group.go(wait=True)
    group.stop()
    rospy.sleep(1)

    #7. release the cube
    print'Release the cube'
    open()





































