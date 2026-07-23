#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  7 11:48:32 2025

@author: labserver
"""
import time
import rclpy
from rclpy.node import Node
#from std_msgs.msg import String  # Ajusta el tipo de mensaje según tus necesidades
from std_msgs.msg import Int32, String, Float32, Bool
from samuchair_interfaces.srv import ArduinoMotor
 # Asegúrate de que la ruta de importación sea correcta
from samuchair import gpioRaspberry
import math
from datetime import datetime


""" gpio 16 láser trasero
gpio 19 láser delantero
gpio 21 led verde más cercano al led rojo
gpio 22 led azul """

laserTrasero = 16
laserDelantero = 19
ledVerde = 20
ledAzul = 21

class  mainNode(Node):
    def __init__(self):
        super().__init__('mainNode')
        self.laser_tras = gpioRaspberry.Puerto()
        self.laser_del = gpioRaspberry.Puerto()
        self.led_verde = gpioRaspberry.Puerto()
        self.led_azul = gpioRaspberry.Puerto()
        self.laser_tras.pinModeOut(laserTrasero)
        self.laser_del.pinModeOut(laserDelantero)
        #self.led_verde.pinModeOut(ledVerde)
        #self.led_azul.pinModeOut(ledAzul)
        ###Variables chatGPT
        # Últimos valores enviados al controlador
        self.last_xMap = 160
        self.last_yMap = 160
        self.last_x = 160
        self.last_y = 160
        # Suavizado
        self.smooth_x = 160.0
        self.smooth_y = 160.0

   #    self.timer = self.create_timer(2, self.timer_callback)  # Llama a la función cada segundo
        self.subJoy = self.create_subscription(
            Int32, "jBnode", self.callback_subJoy, 10)
        
   #     self.subMovilHash = self.create_subscription(
   #         Int32,"name_movil_hash", self.callback_subMovilHash,10)     #Creo subscripción al hash para ROS2BAG
        self.subMovilName = self.create_subscription(
            String,"name_movil", self.callback_subMovilName,10)     #Creo subscripción al nombre para ROS2BAG
        self.subMovilTipo = self.create_subscription(
            String, "tipo_exp", self.callback_subMovilTipo, 10)
        self.subMovilModo = self.create_subscription(
            String, "modo_exp", self.callback_subMovilModo, 10)
        self.subMovilEjecucion = self.create_subscription(
            Int32, "Ejecucion", self.callback_subMovilEjecucion, 10)
        self.client = self.create_client(
            ArduinoMotor,
            'control_joystick' 
        )
        self.subOpasistida = self.create_subscription(
            Int32, "op_manual_asistida", self.callback_subOpasistida, 10)

        self.timer = self.create_timer( 1.0, self.callback_timer )

        #Creamos un publicador para controlar la grabación
        self.grab = self.create_publisher(Bool, 'control_grabacion', 10)
        #Ahora otro publicador para indicar los detalles del directorio de grabación
        self.nombre_grab = self.create_publisher(String,'directorio_grabacion',10)
        #Variables que se actualizan con la información del directorio donde se
        self.dir_grab_hash = None   # Sin uso
        self.dir_grab_modo = None
        self.dir_grab_tipo = None
        self.dir_grab_total = None  #El nombre del directorio. Contiene usuario, mdo y tipo
        self.dir_grab_name  = None  #Este es el nombre del usuario sin espacios (debe tener más de 2 caracteres)
        self.grab_encurso = False   #Identifica si una grabación está o no en curso (sin uso)


        self.JBnodeCommand = None
        self.tipo_expCommand = None
        self.modo_expCommand = None
        self.EjecucionCommand = None
        self.bluetoothConnected = False


        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Esperando...")

        self.req = ArduinoMotor.Request()

    def __del__(self):
        """Asegura que la cámara se cierre cuando el objeto es destruido."""
        super().destroy_node()

    def callback_timer( self ):
        if self.modo_expCommand == "Modo:1":
            if self.bluetoothConnected == True:
                pass
    def callback_subOpasistida( self, indata):
        self.opaAsis = indata.data
        if self.modo_expCommand == "Modo:2":
            if self.client.service_is_ready():
                x, y = self.map_joystick_to_motor(self.opaAsis)
                self.req.command = "velocidad"  
                self.req.x = x
                self.req.y = y
                self.future = self.client.call_async(self.req)
                self.future.add_done_callback(self.callback_handleServiceResponse)
        
    def callback_subJoy(self,indata):
        self.JBnodeCommand = indata.data
        if self.JBnodeCommand != -1:
            self.bluetoothConnected = True
        else:
            self.bluetoothConnected = False
        #Descomentar uso joystick analógico
        """ if self.JBnodeCommand >= 0:
            x = (self.JBnodeCommand >> 8) & 0xFF
            y = self.JBnodeCommand & 0xFF """
        #self.get_logger().info(f'Comando Joystick Bluetooth: {self.JBnodeCommand}')
        if self.bluetoothConnected and self.modo_expCommand == "Modo:1" and self.JBnodeCommand is not None:
            if self.client.service_is_ready():
                x, y = self.map_joystick_to_motor(self.JBnodeCommand) #descomentar para usar con la cruceta digital
                #x,y = self.map_Joy_to_Controller(x,y) #descomentar para usar joystick analógico
                self.req.command = "velocidad"  
                self.req.x = x
                self.req.y = y
                self.future = self.client.call_async(self.req)
                self.future.add_done_callback(self.callback_handleServiceResponse)


    def map_Joy_to_Controller(self, x, y):

            # -----------------------------
        # CONFIG SISTEMA ANTIGUO
        # -----------------------------
        OLD_CENTER = 160
        SCALE = 0.65

        # -----------------------------
        # CENTRO JOYSTICK NUEVO
        # -----------------------------
        CENTER = 128

        # -----------------------------
        # INVERTIR EJES (según hardware que ya dijiste)
        # -----------------------------
        x = 255 - x
        y = 255 - y

        # -----------------------------
        # 🔥 CORRECCIÓN CRÍTICA: SWAP DE EJES
        # -----------------------------
        x, y = y, x

        # -----------------------------
        # NORMALIZACIÓN
        # -----------------------------
        dx = x - CENTER
        dy = y - CENTER

        DEADZONE = 8
        if abs(dx) < DEADZONE:
            dx = 0
        if abs(dy) < DEADZONE:
            dy = 0

        # -----------------------------
        # ESCALA A SISTEMA ANTIGUO
        # -----------------------------
        xMap = int(OLD_CENTER + dx * SCALE)
        yMap = int(OLD_CENTER + dy * SCALE)

        # -----------------------------
        # LIMITES DEL CONTROLADOR
        # -----------------------------
        xMap = max(40, min(248, xMap))
        yMap = max(80, min(250, yMap))

        # -----------------------------
        # FILTRO SUAVE
        # -----------------------------
        if hasattr(self, "last_x"):
            if abs(xMap - self.last_x) < 3:
                xMap = self.last_x
            if abs(yMap - self.last_y) < 3:
                yMap = self.last_y

        self.last_x = xMap
        self.last_y = yMap

        print(f"[JOY FIXED] new({x},{y}) -> old({xMap},{yMap})")

        return xMap, yMap
    

    #Pruebas con chatGPT
    """ def callback_subJoy(self, indata):
        self.JBnodeCommand = indata.data

        if self.JBnodeCommand != -1:
            self.bluetoothConnected = True
        else:
            self.bluetoothConnected = False

        # 🔥 DECODIFICAR (NUEVO SISTEMA)
        packed = self.JBnodeCommand
        x = packed // 1000
        y = packed % 1000

        self.get_logger().info(f'Joystick -> X:{x} Y:{y}')

        if self.bluetoothConnected and self.modo_expCommand == "Modo:1":
            if self.client.service_is_ready():
                self.req.command = "velocidad"
                self.req.x = x
                self.req.y = y
                self.get_logger().info(f"[SUB] received: {self.JBnodeCommand}")
                self.future = self.client.call_async(self.req)
                self.future.add_done_callback(self.callback_handleServiceResponse) """

    def callback_subMovilName(self,indata):   #Esta función se ha añadido por ajmc para control ros2bag
        self.dir_grab_name = str(indata.data).replace(' ','')
        if self.dir_grab_modo is not None and self.dir_grab_tipo is not None:
            self.dir_grab_total = self.dir_grab_name+'_'+self.dir_grab_tipo+'_'+self.dir_grab_modo
            msg = String()
            timestamp = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
            msg.data = self.dir_grab_total + f"_{timestamp}"
            self.nombre_grab.publish(msg)

  #  def callback_subMovilHash(self,indata):   #Esta función se ha añadido por ajmc para control ros2bag
  #      #Función en desuso, se prefiere incluir el nombre del sujeto
  #      self.dir_grab_hash = str(indata.data)
  #      if self.dir_grab_modo is not None and self.dir_grab_tipo is not None:
  #          self.dir_grab_total = self.dir_grab_hash+'_'+self.dir_grab_tipo+'_'+self.dir_grab_modo
  #          msg = String()
  #          timestamp = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
  #          msg.data = self.dir_grab_total + f"_{timestamp}"
  #          self.nombre_grab.publish(msg)

    def callback_subMovilTipo(self,indata ):
        self.tipo_expCommand = indata.data
        self.get_logger().info(f'Comando Movil Tipo: {self.tipo_expCommand}')
        
        ####A partir de aquí se ha añadido para crear el nombre del directorio donde guardar ros2bag
        self.dir_grab_tipo = indata.data[-1]
        if self.dir_grab_modo is not None and self.dir_grab_name is not None:
            self.dir_grab_total = self.dir_grab_name+'_'+self.dir_grab_tipo+'_'+self.dir_grab_modo
            msg = String()
            timestamp = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
            msg.data = self.dir_grab_total + f"_{timestamp}"
            self.nombre_grab.publish(msg)
           
    
    def callback_subMovilModo(self,indata):
        
        self.modo_expCommand = indata.data 
        
        ####A partir de aquí se ha añadido para crear el nombre del directorio donde guardar ros2bag
        self.dir_grab_modo=indata.data[-1]
        if self.dir_grab_name is not None and self.dir_grab_tipo is not None:
            self.dir_grab_total = self.dir_grab_name+'_'+self.dir_grab_tipo+'_'+self.dir_grab_modo
            msg = String()
            timestamp = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
            msg.data = self.dir_grab_total + f"_{timestamp}"
            self.nombre_grab.publish(msg)
           
        ####Fin de publicación dell nombre del directorio donde guardar

        if self.modo_expCommand == 'Modo:1':
            if self.client.service_is_ready():
                self.req.command = "modo"
                self.req.x = 1
                self.req.y = 0
                self.future = self.client.call_async(self.req)
                self.future.add_done_callback( self.callback_handleServiceResponse)
        elif self.modo_expCommand == 'Modo:2':
            if self.client.service_is_ready():
                self.req.command = "modo"
                self.req.x = 1
                self.req.y = 0
                self.future = self.client.call_async(self.req)
                self.future.add_done_callback( self.callback_handleServiceResponse)
        else:
            if self.client.service_is_ready():
                self.req.command = "modo"
                self.req.x = 0
                self.req.y = 0
                self.future = self.client.call_async(self.req)
                self.future.add_done_callback( self.callback_handleServiceResponse)        
        self.get_logger().info(f'Comando Movil Modo: {self.modo_expCommand}')
    
    def callback_subMovilEjecucion(self,indata):
        self.EjecucionCommand = indata.data
        if self.EjecucionCommand == 20:  #Start
            self.laser_del.digitalWrite(True)
            self.laser_tras.digitalWrite(True)
            # self.led_azul.digitalWrite(True)
            # self.led_verde.digitalWrite(True)
            msg = Bool()
            msg.data = True
            self.grab.publish(msg)
            self.grab_encurso=True   #Arranca la grabación
            
        elif self.EjecucionCommand == 30:  #Stop
            self.laser_del.digitalWrite(False)
            self.laser_tras.digitalWrite(False)
            # self.led_azul.digitalWrite(False)
            # self.led_verde.digitalWrite(False)
            msg=Bool()
            msg.data = False
            self.grab.publish(msg)
            self.grab_encurso=False
        
        
        self.get_logger().info(f'Comando Movil Ejecucion: {self.EjecucionCommand}')

    def callback_handleServiceResponse ( self, indata):
        try:
            resp = indata.result()
            #self.get_logger().info("Estoy en el servicio llamado desde mainNode")
            print(resp)
        except Exception as e:
            self.get_logger().info("estoy en error")
            print(e)
            

    def map_joystick_to_motor(self, comando):
        mapping = {
            0: (160, 160),
            3: (248, 146),
            5: (60, 140),
            9: (147, 250),
            6: (147, 80),
            10: (248, 200),
            12: (248, 130),
            17: (40, 200),
            15: (40, 130),
        }
        return mapping.get(comando, (160, 160))  # Default Parado
    



def main(args=None):
    rclpy.init(args=args)
    node = mainNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        rclpy.shutdown()

if __name__ == '__main__':
    main()
