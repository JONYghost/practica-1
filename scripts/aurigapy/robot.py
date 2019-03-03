#!/usr/bin/env python3


from aurigapy import *
import sensors
import time

##-----Constantes y variables globales-----##

# Estados
STOP                              =  0
MOVING_FORWARD_MAX                =  1
MOVING_FORWARD_PROPORTIONAL       =  2
MOVING_BACKWARD_MAX               =  3
MOVING_BACKWARD_PROPORTIONAL      =  4
PICK_OBJECT                       =  5
UNDEFINED                         = -1


# Codigos de Error
EXECUTION_ERROR         = -1
EXECUTION_SUCCESSFUL    =  0

# Roles
LEADER      = 0
FOLLOWER    = 1
UNDEFINED   = -1

# TODO: Añadir elementos cuando esten todos los sensores
def addSensors(list_of_sensors,self):
        count = 0
        for sensor in list_of_sensors:
            if(sensor == "ultrasonic"):
                self.READ_SENSORS[count] = sensors.readUltraSensor
                self.PROCESS_SENSORS[count] = sensors.processUltrasonicSensorData
                print("Add " + sensor + " sensor")
                count += 1
            elif(sensor == "light"):
                self.READ_SENSORS[count] = sensors.readLightSensor
                self.PROCESS_SENSORS[count] = sensors.processLightSensorData
                print("Add " + sensor + " sensor")
                count += 1

##---------------Clases--------------------##
# Este struct contendrá la información de configuración del robot
class Config:
    def __init__(self):
        print("Init Class Config")

# Este struct contendrá la información raw de los sensores
class Data:
    def __init__(self):
        print("Init Class Data")

# Este struct contendrá la información procesada de los sensores
class Information:
    def __init__(self):
        print("Init Class Information")
        
# Este struct contendrá las salidas que hay que aplicar a cada motor
class Actions:
    def __init__(self):
        print("Init Class Actions")
        
# Clase robot
class Robot:
    def __init__(self,name,mode,bluetooth_path,robot_rol,robot_sensors_list,robot_sensor_ports_list):
        print("Init Class Robot")
        
        self.name = name
        self.mode = mode
        
        if(self.mode == 'real_robot'):
            print(self.name + ": Modo usando el Robot real")
            self.mobile_robot = AurigaPy(debug=False)
            self.mobile_robot.connect(bluetooth_path)
            self.error = EXECUTION_SUCCESSFUL
        
        elif(self.mode == 'simulation'):
            print(self.name + ": Modo de Simulacion")
            self.error = EXECUTION_SUCCESSFUL
        
        else:
            print(self.name + ": Modo no reconocido")
            self.error = EXECUTION_ERROR
        
        # Añadimos información de los structs de datos
        self.st_config = Config()
        self.st_meas = Data() 
        self.st_information = Information()
        self.st_actions = Actions()
        
        self.state = STOP
        self.error = EXECUTION_SUCCESSFUL
        
        if robot_rol == "leader":
            self.rol = LEADER
        elif robot_rol == "follower":
            self.rol = FOLLOWER
        else:
            self.rol = UNDEFINED
            
        self.list_of_sensors = robot_sensors_list
        self.sensor_ports = robot_sensor_ports_list
        
        # Diccionarios de Sensores
        # Permiten hacer la clase más genérica
        self.READ_SENSORS = {0:""}
        self.PROCESS_SENSORS = {0:""}

    
    # Función genérica que debe ir llamando a cada una de las funciones específicas para rellenar el struct de "Data" con 
    # los datos de todos los sensores instalados.
    def readSensors(self):
        for sensor in self.READ_SENSORS:
            self.READ_SENSORS[sensor](self,self.sensor_ports[sensor])

    # Función para extraer la información a partir de los datos 'en crudo'.
    def processData(self):
        for sensor in self.PROCESS_SENSORS:
            self.PROCESS_SENSORS[sensor](self,self.sensor_ports[sensor])
    
    # Funcion para determinar el siguiente estado del Lider
    # TODO: Cambiar la maquina de estados cuando esten todos los sensores
    def leaderFiniteStateMachine(self):
        print(self.name + ": Actualizamos la maquina de estado del lider")
        
        if(self.st_meas):
            self.state = STOP
            
        elif(self.st_meas):
            self.state = MOVING_FORWARD_MAX
            
        elif(self.st_meas):
            self.state = MOVING_FORWARD_PROPORTIONAL
        
        elif(self.st_meas):
            self.state = MOVING_BACKWARD_MAX    
            
        elif(self.st_meas):
            self.state = MOVING_BACKWARD_PROPORTIONAL    
            
        elif(self.st_meas):
            self.state = PICK_OBJECT
        
        else:
            self.state = UNDEFINED
    
    # Funcion para determinar el siguiente estado del Seguidor
    # TODO: Cambiar la maquina de estados cuando esten todos los sensores
    def followerFiniteStateMachine(self):
        print(self.name + ": Actualizamos la maquina de estados del seguidor")
        
        if(self.st_meas):
            self.state = STOP
            
        elif(self.st_meas):
            self.state = MOVING_FORWARD_MAX
            
        elif(self.st_meas):
            self.state = MOVING_FORWARD_PROPORTIONAL
        
        elif(self.st_meas):
            self.state = MOVING_BACKWARD_MAX    
            
        elif(self.st_meas):
            self.state = MOVING_BACKWARD_PROPORTIONAL    
            
        elif(self.st_meas):
            self.state = PICK_OBJECT
        
        else:
            self.state = UNDEFINED
    
    # Función para determinar qué tarea se va a llevar a cabo a partir de la información extraída a partir
    # de los datos de los sensores y del rol del robot. 
    def updateFiniteStateMachine(self):
        
        if(self.rol == LEADER):
            self.leaderFiniteStateMachine()
        
        elif(self.rol == FOLLOWER):
            self.followerFiniteStateMachine()
            
        else:
            self.state = STOP               
            
    # Controlador específico para parar motores
    def controllerStop(self):
        if(self.mode == 'simulation'):
            print(self.name + ": Calculamos la acción de control")
                
    # Función genérica que llama al controlador específico adecuado en función de la tarea
    # que se deba realizar. 
    # TODO: Cambiar el selector del controlador cuando estén los controladores y estados
    def controller(self):
        if(self.state == STOP):
            self.controllerStop()
            
        elif(self.state == MOVING_FORWARD_MAX):
            self.controllerStop()

        elif(self.state == MOVING_FORWARD_PROPORTIONAL):
            self.controllerStop()
            
        elif(self.state == MOVING_BACKWARD_MAX):
            self.controllerStop()
            
        elif(self.state == MOVING_BACKWARD_PROPORTIONAL):
            self.controllerStop()
        
        elif(self.state == PICK_OBJECT):
            self.controllerStop()
        
        elif(self.state == UNDEFINED):
            self.controllerStop()
        
        else:
            self.controllerStop()       

    # Función encargada de pasar a motores los comandos calculados por los controladores
    # este es el último punto antes de actuar sobre los motores,por lo que tenemos que 
    # ser cuidadosos de no enviar valores indeseados
    # TODO: Añadir cuando esten hechos los controladores
    def execute(self):
        if(self.mode == 'simulation'):
            print(self.name + ": Mandamos la acción de control a los actuadores")
        
        self.error = EXECUTION_SUCCESSFUL
        
        if(self.state == UNDEFINED):
            self.error = EXECUTION_ERROR
        if(self.mode == UNDEFINED):
            self.error = EXECUTION_ERROR

    # Función encargada de refrescar la info para el usuario a intervalos de tiempo correctos
    # TODO: Añadir la info util y cuando esté todo hecho
    def refreshUserInterface (self):
        if(self.mode == 'simulation'):
            print(self.name + ": Mostramos la informacion util y los errores")

    # Funcion Loop que hace la llamada a todas las funciones de lectura, procesado, maquina de estados,
    # control y muestra de datos
    def run_main(self):
        addSensors(self.list_of_sensors,self)
        while True:
            # Leemos los sensores
            self.readSensors()
            
            # Extraemos la información a partir de los datos
            self.processData()
            
            # Actualizamos la máquina de estados a partir de la información recibida por los sensores 
            self.updateFiniteStateMachine()
           
            # Calculamos las acciones que tenemos que aplicar a los distintos motores, en función del
            # estado y las lecturas de los sensores
            self.controller()
            
            # Pasamos a motores las acciones calculadas
            self.execute()

            # Publicamos info importante para el debug
            self.refreshUserInterface()
            
            print(self.name + ": --------------------------")
            time.sleep(2) #!!!!!!!!!!!!!!!! ELIMINAR DELAY !!!!!!!!!!!!!!!!#  
        
