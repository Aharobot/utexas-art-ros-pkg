#!/usr/bin/python
#
#  send tele-operation commands to pilot from a joystick
#
#   Copyright (C) 2009 Austin Robot Technology
#
#   License: Modified BSD Software License Agreement
#
#   Author: Jack O'Quin
#
# $Id$

## TODO: add timer loop, so the joystick can accelerate smoothly

PKG_NAME = 'art_nav'

import sys
import os
import roslib;
roslib.load_manifest(PKG_NAME)

import rospy
from art_nav.msg import CarCommand
from art_nav.msg import CarCommandStamped
from joy.msg import Joy

# global constants
max_wheel_angle = 29.0                  # degrees
max_speed = 6.0                         # meters/second
max_speed_reverse = -3.0                # meters/second

class JoyNode():
    "Vehicle joystick tele-operation node."

    def __init__(self):
        "JoyNode constructor"
        self.car_cmd = CarCommand()
        self.car_msg = CarCommandStamped()

        self.steer = 0                  # steering axis (left)
        self.speed = 1                  # speed axis (left)
        self.direction = 1.0            # gear direction (drive)

        rospy.init_node('joy_teleop')
        self.topic = rospy.Publisher('pilot/cmd', CarCommandStamped)
        self.joy = rospy.Subscriber('joy', Joy, self.joyCallback)

        self.car_msg.header.stamp = rospy.Time.now()
        self.car_msg.command = self.car_cmd
        self.topic.publish(self.car_msg)

    def joyCallback(self, joy):
        "invoked every time a joystick message arrives"
        rospy.logdebug('joystick input:\n' + str(joy))

        # handle various buttons (when appropriate)
        if joy.buttons[0] and self.car_cmd.velocity == 0.0:
            if self.direction != -1.0:
                self.direction = -1.0       # shift to reverse
                rospy.loginfo('shifting to reverse')

        elif joy.buttons[1]:
            if self.car_cmd.velocity != 0.0:
                rospy.logwarn('emergency stop')
            self.car_cmd.velocity = 0.0     # stop car immediately

        elif joy.buttons[2] and self.car_cmd.velocity == 0.0:
            if self.direction != 1.0:
                self.direction = 1.0        # shift to drive
                rospy.loginfo('shifting to drive')

        elif joy.buttons[10]:               # select left joystick
            self.steer = 0                  #  steering axis
            self.speed = 1                  #  speed axis
            rospy.loginfo('left joystick selected')

        elif joy.buttons[11]:               # select right joystick
            self.steer = 3                  #  steering axis
            self.speed = 2                  #  speed axis
            rospy.loginfo('right joystick selected')

        else:                               # normal analog control
            # set steering angle
            self.setAngle(joy.axes[self.steer])
            # adjust speed
            self.adjustSpeed(joy.axes[self.speed])

        self.car_msg.header.stamp = rospy.Time.now()
        self.car_msg.command = self.car_cmd
        self.topic.publish(self.car_msg)

    def adjustSpeed(self, dv):
        "accelerate dv meters/second/second"

        dv *= 0.1

        # take absolute value of velocity
        vabs = self.car_cmd.velocity * self.direction

        # never shift gears via speed controller, stop at zero
        if -dv > vabs:
            vabs = 0.0
        else:
            vabs += dv

        self.car_cmd.velocity = vabs * self.direction

        # ensure forward and reverse speed limits never exceeded
        if self.car_cmd.velocity > max_speed:
            self.car_cmd.velocity = max_speed
        elif self.car_cmd.velocity < max_speed_reverse:
            self.car_cmd.velocity = max_speed_reverse

    def setAngle(self, turn):
        "set wheel angle"

        # use cube of range [-1..1] turn command to improve
        # sensitivity while retaining sign
        self.car_cmd.angle = turn * turn * turn * max_wheel_angle

        # ensure maximum wheel angle never exceeded
        if self.car_cmd.angle > max_wheel_angle:
            self.car_cmd.angle = max_wheel_angle
        elif self.car_cmd.angle < -max_wheel_angle:
            self.car_cmd.angle = -max_wheel_angle

def main():

    joynode = JoyNode()
    rospy.loginfo('joystick vehicle controller starting')
    try:
        rospy.spin()
    except rospy.ROSInterruptException: pass
    rospy.loginfo('joystick vehicle controller finished')

if __name__ == '__main__':
    # run main function and exit
    sys.exit(main())
