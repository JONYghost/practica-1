from aurigapy import *

def follow_line(robot):
    if (robot.mode == 'real_robot')
        val_detection = robot.st_information.line_detection
        if(value == 0):
            robot.controllerMovingFWD_MAX()
        if(value == 1):
            robot.controllerMovingLeft()
        if(value == 2):
            robot.controllerMovingRight()
        else:
            robot.controllerStop()
