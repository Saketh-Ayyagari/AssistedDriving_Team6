import sys

# If this file is nested inside a folder in the labs folder, the relative path should
# be [1, ../../library] instead.
sys.path.insert(1, '../../library')
import racecar_core
import racecar_utils as rc_utils

########################################################################################
# Global variables
########################################################################################
global speed, angle

rc = racecar_core.create_racecar()


# Access the most recent lidar scan.
scan = rc.lidar.get_samples()

# Get the distance of the measurement directly in front of the car
forward_distance = scan[0]


def start():
   global speed, angle
   speed = 0
   angle = 0

   rc.drive.stop()

def update():




if __name__ == '__main__':
   rc.set_start_update(start, update)
   rc.go()