#!/usr/bin/env python3


## Este script se encarga de recoger los controladores

from aurigapy import *
import time

#TODO: Añadir las funiones que vayan haciendo paco y abel
#Todo lo que hay hasta el momento son EJEMPLOS (cambiad lo que os parezca)

#Distancia -ultrasonidos
IMPOSSIBLE_DISTANCE = -1.0
MIN_ULTRA_VALUE = 0 #Minimum detectable value for the distance sensor
MAX_ULTRA_VALUE = 400 #Maximum detectable value for the distance sensor
NEAR_OBJECT_THRESHOLD = 10 #An object closer than this will be considered a "near object"
FAR_OBJECT_THRESHOLD = 250 #An object closer than this will be considered a "far object"
NO_OBJECT_DETECTED = 0
NEAR_OBJECT_DETECTED = 1
FAR_OBJECT_DETECTED = 2

FWD_MAX = 180
BWD_MAX = 140
FWD_MIN = 60
BWD_MIN = 20
DEG_DEFAULT = 3600

# Este struct contendrá las salidas que hay que aplicar a cada motor
class Actions:
    def __init__(self):
        print("Init Class Actions")
        
        self.movement_motors_pwm = 0
        self.command = "forward"
        self.tool_motor_pwm = 0


##------------------CONTROLADORES------------------##        

def controllerStop(robot):
	if(robot.mode == 'simulation'):
    	print(robot.name + ": Calculamos la acción de control - Stop")
    	robot.state = STOP
	else:
    	robot.move_to(command="forward", degrees=10000, speed=0)
    	robot.state = STOP

def controllerMovingForward(robot,speedo):
	if(robot.mode == 'simulation'):
    	print(robot.name + ": Calculamos la acción de control - Forward")
    	robot.state = MOVING_FORWARD_MAX
	else:
    	robot.move_to(command="forward", degrees=3600, speed=speedo)
    	robot.state = MOVING_FORWARD_MAX

def controllerMovingBackward(robot,speedo):
	if(robot.mode == 'simulation'):
    	print(robot.name + ": Calculamos la acción de control - Backward")
    	robot.state = MOVING_BACKWARD_MAX
	else:
    	robot.move_to(command="backward", degrees=3600, speed=speedo)
    	robot.state = MOVING_BACKWARD_MAX

def controllerMovingLeft(robot):
	if(robot.mode == 'simulation'):
    	print(robot.name + ": Calculamos la acción de control - Left")
    	robot.state = UNDEFINED
	else:
    	robot.move_to(command="left", degrees=3600, speed=80)
    	robot.state = UNDEFINED
        
def controllerMovingRight(robot):
	if(robot.mode == 'simulation'):
    	print(robot.name + ": Calculamos la acción de control - Left")
    	robot.state = UNDEFINED
	else:
    	robot.move_to(command="left", degrees=3600, speed=80)
    	robot.state = UNDEFINED
    
# Controlador para velocidad proporcional según distancia
def controllerProportional(robot):
    PROP_SPEED = 0
    if(robot.mode == 'simulation'):
        print(robot.name + ": Calculamos la acción de control - Proportional Speed")
    elif(robot.mode == 'real_robot'):
        if(# lectura siguelíneas = recto/perdido)
            if(robot.st_data.ultrasensor_distance < NEAR_OBJECT_THRESHOLD):
                # Move slowly
                robot.move_to(command="forward", degrees=DEG_DEFAULT, speed=FWD_MIN)
            elif(robot.st_data.ultrasensor_distance > FAR_OBJECT_THRESHOLD):
                # Move hastely
                robot.move_to(command="forward", degrees=DEG_DEFAULT, speed=FWD_MAX)
            elif(robot.st_data.ultrasensor_distance > NEAR_OBJECT_THRESHOLD and robot.st_data.ultrasensor_distance < FAR_OBJECT_THRESHOLD):
                PROP_SPEED = robot.st_data.ultrasensor_distance-NEAR_OBJECT_THRESHOLD)/2
                # dist_sensor_recogida-dist_minima/2
                robot.move_to(command="forward", degrees=DEG_DEFAULT, speed=(PROP_SPEED)
                              
        elif(# lectura siguelíneas = derecha)                  
            elif(robot.st_data.ultrasensor_distance < NEAR_OBJECT_THRESHOLD):
                # Move slowly
                robot.move_to(command="right", degrees=DEG_DEFAULT, speed=FWD_MIN)
            elif(robot.st_data.ultrasensor_distance > FAR_OBJECT_THRESHOLD):
                # Move hastely
                robot.move_to(command="right", degrees=DEG_DEFAULT, speed=FWD_MAX)
            elif(robot.st_data.ultrasensor_distance > NEAR_OBJECT_THRESHOLD and robot.st_data.ultrasensor_distance < FAR_OBJECT_THRESHOLD):
                PROP_SPEED = robot.st_data.ultrasensor_distance-NEAR_OBJECT_THRESHOLD)/2
                # dist_sensor_recogida-dist_minima/2
                robot.move_to(command="right", degrees=DEG_DEFAULT, speed=(PROP_SPEED)
                              
        elif(# lectura siguelíneas = izquierda)                  
            elif(robot.st_data.ultrasensor_distance < NEAR_OBJECT_THRESHOLD):
                # Move slowly
                robot.move_to(command="left", degrees=DEG_DEFAULT, speed=FWD_MIN)
            elif(robot.st_data.ultrasensor_distance > FAR_OBJECT_THRESHOLD):
                # Move hastely
                robot.move_to(command="left", degrees=DEG_DEFAULT, speed=FWD_MAX)
            elif(robot.st_data.ultrasensor_distance > NEAR_OBJECT_THRESHOLD and robot.st_data.ultrasensor_distance < FAR_OBJECT_THRESHOLD):
                PROP_SPEED = robot.st_data.ultrasensor_distance-NEAR_OBJECT_THRESHOLD)/2
                # dist_sensor_recogida-dist_minima/2
                robot.move_to(command="left", degrees=DEG_DEFAULT, speed=(PROP_SPEED)
            
    robot.st_actions.movement_motors_pwm = robot.st_config.max_speed_pwm_value
    robot.st_actions.command = "forward"
