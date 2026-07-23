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
from samuchair import gpioRaspberry

tactilDerecho = 17
tactilIzquierdo = 27


class tactilesNode(Node):
    def __init__(self):
        super().__init__('st_node')
        
        self.tactil_izq = gpioRaspberry.Puerto() 
        self.tactil_der = gpioRaspberry.Puerto() 
        self.tactil_izq.pinModeIn(tactilIzquierdo)
        self.tactil_der.pinModeIn(tactilDerecho)
        self.publisher_tactil_izq = self.create_publisher(Int32, 'tactil_izq', 10)
        self.publisher_tactil_der = self.create_publisher(Int32,'tactil_der',10)
        self.timer = self.create_timer(0.5,self.timer_callback)

    def timer_callback(self):
        msg =Int32()
        #Poner aquí la lectura d elos táctiles
        msg.data = self.tactil_izq.digitalRead()
        self.publisher_tactil_izq.publish(msg)
        #self.get_logger().info(f'Dato publicado Táctil Izquierdo: {msg.data}')
        msg.data = self.tactil_der.digitalRead()
        self.publisher_tactil_der.publish(msg)
        #self.get_logger().info(f'Dato publicado Táctil Derecho: {msg.data}')
   


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
