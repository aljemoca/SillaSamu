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

from samuchair import ComESP32


class esp32Node(Node):
    def __init__(self):
        super().__init__('esp32_node')
        self.port = "/dev/esp32_sensor"
        self.esp32 = ComESP32.ComESP32(self.port)  # Ajusta el puerto según corresponda
        self.publisher_pot = self.create_publisher(Int32, 'pot_esp32', 10)
        self.publisher_leftwheel = self.create_publisher(Int32,'left_wheel_steps',10)
        self.publisher_rightwheel = self.create_publisher(Int32,'right_wheel_steps',10)
        self.timer = self.create_timer(1.0, self.timer_callback)  # Llama a la función cada segundo


    def timer_callback(self):
        datos = self.esp32.obtenerMedidas()
        if not datos[0]:
            msg = Int32()
            msg.data = datos[1]
            self.publisher_pot.publish(msg)
            self.get_logger().info(f'Dato publicado Pot: {msg.data}')
            msg.data = datos[3][0]
            self.publisher_leftwheel.publish(msg)
            self.get_logger().info(f'Dato publicado LW: {msg.data}')
            msg.data = datos[3][1]
            self.publisher_rightwheel.publish(msg)
            self.get_logger().info(f'Dato publicado RW: {msg.data}')

    def destroy_serial(self):
        del self.esp32

def main(args=None):
    rclpy.init(args=args)
    node = esp32Node()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_serial()  # Asegúrate de cerrar la conexión serial
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
