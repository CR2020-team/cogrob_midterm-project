#!/usr/bin/python
"""
This node coordinates the executions of the Head Node and the Camera Node,
as the images need to be taken when the head is in proper positions.
"""

import rospy
from naoqi_driver.naoqi_node import NaoqiNode
from pepper_msgs.srv import LookAt
from pepper_msgs.srv import TakePicture
from std_msgs.msg import Int8

"""Class used as an abstraction of the Node"""
class MasterNode(NaoqiNode):

  __slots__ = 'motionProxy'

  def __init__(self):
    """
    Constructor. Creates the node and connects it to the NaoQi interface.
    """
    NaoqiNode.__init__(self, 'master_node')
    self.connectNaoQi()

  def connectNaoQi(self):
    """
    Connects the node to the NaoQi interface. The parameters pip and pport are stored in the parameter server.
    The Proxy used is ALRobotPosture, in order to make the robot go to the "StandInit" posture
    at the beginning and at the end of the execution.
    """
    self.pip = rospy.get_param('pip')
    self.pport = rospy.get_param('pport')
    rospy.loginfo("MasterNode connecting to NaoQi at %s:%d", self.pip, self.pport)
    self.motionProxy = self.get_proxy("ALRobotPosture")
    if self.motionProxy is None:
      exit(1)
    rospy.loginfo("ALRobotPosture successful!")
      
  def start(self):
    """
    Actual execution of the node.
    The directions (right, front, left) are represented as integers (-1, 0, 1).
    The services LookAt and TakePicture are called successively for each direction.
    In particular, the TakePicture service must be called when the LookAt service response is True.
    """
    self.motionProxy.goToPosture("StandInit", 1.0)
    for direction in [-1, 0, 1]:
      # Look at right, front, left
      ret = self._look_at(direction)
      if not ret:
        exit(1)
      # Take picture
      ret = self._take_picture(direction)
      if not ret:
        exit(1)
      # Wait
      rospy.sleep(rospy.Duration(2.0))
    self.motionProxy.goToPosture("StandInit", 1.0)

  def _look_at(self, direction):
    """
    Calls the LookAt service.
    The request is the current direction.
    The response is the success of the service.
    """
    service = rospy.get_param('look_at_service')
    rospy.wait_for_service(service)
    try:
      look_at = rospy.ServiceProxy(service, LookAt)
      return look_at(direction).ready
    except rospy.ServiceException as e:
      print("Service call failed: %s" % e)
      return False

  def _take_picture(self, direction):
    """
    Calls the TakePicture service.
    The request is the current direction.
    The response is the success of the service.
    """
    service = rospy.get_param('take_picture_service')
    rospy.wait_for_service(service)
    try:
      take_picture = rospy.ServiceProxy(service, TakePicture)
      return take_picture(direction).ready
    except rospy.ServiceException as e:
      print("Service call failed: %s" % e)
      return False


def main():
  """Creates and executes the node."""
  MasterNode().start()
  try:
    rospy.spin()
  except (KeyboardInterrupt, rospy.exceptions) as e:
    rospy.loginfo("shutdown: %s" % e)


if __name__ == "__main__":
  main()
