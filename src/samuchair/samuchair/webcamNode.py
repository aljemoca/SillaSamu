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
from std_msgs.msg import Int32
 # Asegúrate de que la ruta de importación sea correcta

from samuchair import Webcam


class webcamNode(Node):
    def __init__(self):
        super().__init__('webcam_node')
        self.webcam = Webcam.Webcam()  # Ajusta el puerto según corresponda
        self.publisher_frame = self.create_publisher(Int32, 'frame', 10)
        self.timer = self.create_timer(2, self.timer_callback)  # Llama a la función cada segundo



    def __del__(self):
        """Asegura que la cámara se cierre cuando el objeto es destruido."""
        if hasattr(self, 'webcam') and self.webcam.isOpened():
            self.destroy_webcam()
            print("Cámara liberada por el destructor.")
        super().destroy_node()

    def timer_callback(self):
        frame = self.webcam.tomar_foto()
        msg = Int32()
        msg.data = int(frame)
        self.publisher_frame.publish(msg)
        self.get_logger().info(f'Frame: {msg.data}')
 
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
