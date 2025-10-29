#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  7 11:48:32 2025

@author: labserver
"""

import rclpy
from rclpy.node import Node
from rclpy.time import Time
from rclpy.clock import ClockType
from std_msgs.msg import String  # Ajusta el tipo de mensaje según tus necesidades
from std_msgs.msg import Int32,Float32
 # Asegúrate de que la ruta de importación sea correcta

import threading
import time



class Tactil:
    def __init__(self,a=1):
        self.pinMode(a)
        self.value=0
      #  self.temp_value=0
      #  self.counter=0
      #  self.hilo = threading.Thread(target=self._hilo_callback)
      #  self.hilo.start()
      

    def pinMode(self,a=1):
        a=1   

    def digitalRead(self):
        return int(self.value)
    #
    #def _hilo_callback(self):
    #    self.counter=self.counter+1
    #    print('.')
    #    if self.counter==5:
    #        self.counter=0
        #time.sleep(0.5)  #Cambiar a 0.1



class tactilesNode(Node):
    def __init__(self):
        super().__init__('st_node')
        self.tactil_izq = Tactil() 
        self.tactil_der = Tactil() 
        self.publisher_tactil_izq = self.create_publisher(Int32, 'tactil_izq', 10)
        self.publisher_tactil_der = self.create_publisher(Int32,'tactil_der',10)
        self.timer = self.create_timer(0.5,self.timer_callback)

    def timer_callback(self):
        msg =Int32()
        #Poner aquí la lectura d elos táctiles
        msg.data = self.tactil_izq.digitalRead()
        self.publisher_tactil_izq.publish(msg)
        self.get_logger().info(f'Dato publicado Táctil Izquierdo: {msg.data}')
        msg.data = self.tactil_der.digitalRead()
        self.publisher_tactil_der.publish(msg)
        self.get_logger().info(f'Dato publicado Táctil Derecho: {msg.data}')
   


def main(args=None):
    rclpy.init(args=args)
    node = tactilesNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        #node.destroy_webcam()  
        rclpy.shutdown()

if __name__ == '__main__':
    main()
