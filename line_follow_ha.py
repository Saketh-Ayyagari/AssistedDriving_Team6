"""
MIT BWSI Autonomous RACECAR
MIT License
racecar-neo-prereq-labs

File Name: lab1.py

Title: Lab 1 - RACECAR Controller with best attempt for line following

Author: Team 8: Saketh, Chris, Sophie, Cian

Purpose: Using a Python script and the data polled from the controller module,
write code to replicate a manual control scheme for the RACECAR. Gain a mastery
in using conditional statements, controller functions and an understanding in the
rc.drive.set_speed_angle() function. Complete the lines of code under the #TODO indicators 
to complete the lab.

Expected Outcome: When the user runs the script, they are able to control the RACECAR
using the following keys:
- When the right trigger is pressed, the RACECAR drives forward
- When the left trigger is pressed, the RACECAR drives backward
- When the left joystick's x-axis has a value of greater than 0, the RACECAR's wheels turns to the right
- When the left joystick's x-axis has a value of less than 0, the RACECAR's wheels turns to the left
- When the "A" button is pressed, increase the speed and print the current speed to the terminal window
- When the "B" button is pressed, reduce the speed and print the current speed to the terminal window
- When the "X" button is pressed, increase the turning angle and print the current turning angle to the terminal window
- When the "Y" button is pressed, reduce the turning angle and print the current turning angle to the terminal window

Environment: Test your code using the level "Neo Labs > Lab 1: RACECAR Controller".
"""

########################################################################################
# Imports
########################################################################################

import sys

# If this file is nested inside a folder in the labs folder, the relative path should
# be [1, ../../library] instead.
sys.path.insert(1, '../../library')
import racecar_core
import racecar_utils as rc_utils

########################################################################################
# Global variables
########################################################################################

rc = racecar_core.create_racecar()

# Declare any global variables here
global speed
global angle
global speed_offset
global angle_offset
global contour_center

########################################################################################
# Functions
########################################################################################


# [FUNCTION] The start function is run once every time the start button is pressed
def update_contour():
   global contour_center
   image = rc.camera.get_color_image()
   CROP = ((360, 0), (rc.camera.get_height()-15, rc.camera.get_width()))
   image = rc_utils.crop(image, CROP[0], CROP[1])
   HSV = ((80, 125, 50), (120, 255, 255))
   contours = rc_utils.find_contours(image, HSV[0], HSV[1])
   max_contour = rc_utils.get_largest_contour(contours)
   contour_center = rc_utils.get_contour_center(max_contour)
   rc_utils.draw_contours(color_image=image, contour=max_contour, color=(0, 255, 0))
   rc.display.show_color_image(image)


def line_follow():
   global contour_center
   global angle
   update_contour()
   SETPOINT = rc.camera.get_width()//2
   if contour_center is not None:
      error = SETPOINT - contour_center[1]
      angle = rc_utils.remap_range(error, -320, 320, 1, -1)


def start():
    global speed
    global angle

    speed = 0.0 # The initial speed is at 1.0
    angle = 0.0 # The initial turning angle is 0.0

    # This tells the car to begin at a standstill
    rc.drive.stop()

# [FUNCTION] After start() is run, this function is run once every frame (ideally at
# 60 frames per second or slower depending on processing speed) until the back button
# is pressed  
def update():
   global speed
   global angle
   
   
   right = rc.controller.get_trigger(rc.controller.Trigger.RIGHT)
   left = rc.controller.get_trigger(rc.controller.Trigger.LEFT)
   if right > 0:
      speed = right
   elif left > 0:
      speed = -left
   else:
      speed = 0

   angle, __ = rc.controller.get_joystick(rc.controller.Joystick.LEFT)
   if rc.controller.is_down(rc.controller.Button.A):
      line_follow()
   # Send the speed and angle values to the RACECAR
   rc.drive.set_speed_angle(speed, angle)

########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update)
    rc.go()
