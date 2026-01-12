#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  7 11:48:32 2025

@author: labserver
"""
import time
import rclpy
from rclpy.node import Node
from std_msgs.msg import String  # Ajusta el tipo de mensaje según tus necesidades
from std_msgs.msg import Int32, String, Float32
from samuchair_interfaces.srv import ArduinoMotor
 # Asegúrate de que la ruta de importación sea correcta
from samuchair import gpioRaspberry

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
        self.led_verde.pinModeOut(ledVerde)
        self.led_azul.pinModeOut(ledAzul)

   #    self.timer = self.create_timer(2, self.timer_callback)  # Llama a la función cada segundo
        self.subJoy = self.create_subscription(
            Int32, "jBnode", self.callback_subJoy, 10)
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

        self.timer = self.create_timer( 1.0, self.callback_timer )

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
                
    def callback_subJoy(self,indata):
        self.JBnodeCommand = indata.data
        if self.JBnodeCommand != -1:
            self.bluetoothConnected = True
        else:
            self.bluetoothConnected = False
        self.get_logger().info(f'Comando Joystick Bluetooth: {self.JBnodeCommand}')
        if self.bluetoothConnected and self.modo_expCommand == "Modo:1" and self.JBnodeCommand is not None:
            if self.client.service_is_ready():
                x, y = self.map_joystick_to_motor(self.JBnodeCommand)
                self.req.command = "velocidad"  
                self.req.x = x
                self.req.y = y
                self.future = self.client.call_async(self.req)
                self.future.add_done_callback(self.callback_handleServiceResponse)
    
    def callback_subMovilTipo(self,indata ):
        self.tipo_expCommand = indata.data
        
        self.get_logger().info(f'Comando Movil Tipo: {self.tipo_expCommand}')
    
    def callback_subMovilModo(self,indata):
        
        self.modo_expCommand = indata.data 
        
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
        if self.EjecucionCommand == 20:
            self.laser_del.digitalWrite(True)
            self.laser_tras.digitalWrite(True)
            # self.led_azul.digitalWrite(True)
            # self.led_verde.digitalWrite(True)
        else:
            self.laser_del.digitalWrite(False)
            self.laser_tras.digitalWrite(False)
            # self.led_azul.digitalWrite(False)
            # self.led_verde.digitalWrite(False)
        
        self.get_logger().info(f'Comando Movil Ejecucion: {self.EjecucionCommand}')

    def callback_handleServiceResponse ( self, indata):
        try:
            resp = indata.result()
            self.get_logger().info("Estoy en el servicio llamado desde mainNode")
            print(resp)
        except Exception as e:
            self.get_logger().info("estoy en error")
            print(e)
            

    def map_joystick_to_motor(self, comando):
        mapping = {
            0: (160, 160),
            3: (255, 145),
            5: (0, 138),
            9: (147, 240),
            6: (147, 15),
            10: (255, 191),
            12: (255, 65),
            17: (0, 65),
            15: (0, 191),
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
