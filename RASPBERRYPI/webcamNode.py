#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  7 11:48:32 2025

@author: labserver
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String  # Ajusta el tipo de mensaje según tus necesidades
from std_msgs.msg import Int32
 # Asegúrate de que la ruta de importación sea correcta

from Webcam import Webcam


class webcamNode(Node):
    def __init__(self):
        super().__init__('webcam_node')
        self.webcam = Webcam.Webcam(self.port)  # Ajusta el puerto según corresponda
        self.publisher_frame = self.create_publisher(Int32, 'frame', 10)
        self.timer = self.create_timer(1.5, self.timer_callback)  # Llama a la función cada segundo


    def timer_callback(self):
        frame = self.webcam.tomar_foto()
        msg = Int32()
        msg.data = frame
        self.publisher_frame.publish(msg)
        self.get_logger().info(f'Dato publicado Pot: {msg.data}')
 
    def destroy_webcam(self):
        self.webcam.parar()
        del self.webcam

def main(args=None):
    rclpy.init(args=args)
    node = webcamNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_webcam()  
        rclpy.shutdown()

if __name__ == '__main__':
    main()
