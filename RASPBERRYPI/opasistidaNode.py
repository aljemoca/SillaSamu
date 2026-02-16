#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 10:11:17 2026

@author: alberto
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String,Int32

'''
Este nodo define el modo de funcionamiento operado por los táctiles.
Para ello, genera subscripción a los tópicos 'tactil_izq', 'tactil_der' y 'pot_esp32'
Por tanto, recibe información del estado de los táctiles y del potenciómetro
    OJO: Habrá que hacer que el estado del potenciómetro se publique siempre. 
         Ahora solo se publica cuando hay un cambio de valor

El potenciómetro envía un valor entre 0-9. Dicho valor se cuantifica en tres
niveles:0,1,2. El 0, que sería cuando el potenciómetro está a la izquierda,
representa marcha atrás, el 1 parado y el 2 marcha adelante.

En función del estado de los táctiles, se generan los comandos de navegación
como si del Joystick Bluetooth se tratara (adelante, atrás, giro , etc.). Un total de 
9 opciones que se guardan en la variable nav, con los mismos valores que hace 
el JoystickBluetooth. 

El nodo define un temporizador que cada 0.5 ejecuta la función de navegación que,
en función del etado de los tactiles y el potenciometro, determinar el valor de nav,
que se publica en un nuevo tópico.


# =============================================================================
# def map_joystick_to_motor(self, comando):
#         mapping = {
#             0: (160, 160),
#             3: (255, 145),
#             5: (0, 138),
#             9: (147, 240),
#             6: (147, 15),
#             10: (255, 191),
#             12: (255, 65),
#             17: (0, 65),
#             15: (0, 191),
#         }
# 
# 
# =============================================================================

'''

class opasistidaNode(Node):
    def __init__(self):
        super().__init__('nodo_asincrono')

        # 1. Variables para almacenar el último dato de cada tópico
        self.tactil_izq = None
        self.tactil_der =None
        self.pot = 5
        self.pot_3 = None
        self.nav = 0   # Parado por defecto 
        self.nav_old=-1

        # 2. Suscriptores
        self.create_subscription(Int32, 'tactil_izq', self.update_tactil_izq, 10)
        self.create_subscription(Int32, 'tactil_der', self.update_tactil_der, 10)
        self.create_subscription(Int32, 'pot_esp32', self.update_pot, 10)

        # 3. Publicador
        # self.timer = self.create_timer(0.5,self.timer_callback)
        self.pub = self.create_publisher(Int32, 'op_manual_asistida', 10)

    def update_tactil_izq(self, msg):
        self.tactil_izq = msg.data
        self.timer_callback()
        #self.get_logger().info(f'Dato publicado tactil izquierda: {msg.data}')
    def update_tactil_der(self, msg):
        self.tactil_der = msg.data
        #self.get_logger().info(f'Dato publicado tactil derecha: {msg.data}')
        self.timer_callback()
        
    def timer_callback(self):
        msg = Int32()
        self.navegacion()
        msg.data = self.nav
        if self.nav != self.nav_old:
            self.pub.publish(msg)
            #self.get_logger().info(f'Dato publicado Navegación Táctil: {msg.data}')
            self.nav_old = self.nav
        
    def navegacion(self):
        if  (self.tactil_izq == 0 and self.tactil_der ==0):
            self.nav = 0   #Parado
        else:
            if self.tactil_izq == 1 and self.tactil_der==1 and self.pot_3 == 2:
                self.nav =	3  #Adelante
            if self.tactil_izq == 1 and self.tactil_der==1 and self.pot_3 == 0:
                self.nav = 5  #Atrás
            if self.tactil_izq == 1 and self.tactil_der==0 and self.pot_3 == 2:
                self.nav = 10  #Derecha avance
            if self.tactil_izq == 1 and self.tactil_der==0 and self.pot_3 == 0:
                self.nav =  15 #Derecha atrás
            if self.tactil_izq == 1 and self.tactil_der==0 and self.pot_3 == 1:
                self.nav = 9  #Derecha quieto
            if self.tactil_izq == 0 and self.tactil_der==1 and self.pot_3 == 2:
                self.nav = 12  #Izquierda avance
            if self.tactil_izq == 0 and self.tactil_der==1 and self.pot_3 == 0:
                self.nav =  17 #Izquierda atrás
            if self.tactil_izq == 0 and self.tactil_der==1 and self.pot_3 == 1:
                self.nav =  6 #Izquierda quieta
                
  
    def update_pot(self, msg):
        self.pot = msg.data
        if self.pot < 2: 
            self.pot_3 = 0
        elif self.pot > 7:
            self.pot_3 = 2
        else:
            self.pot_3 = 1
        #self.get_logger().info(f'Dato publicado potenciometro: {self.pot_3}')
        self.timer_callback()
def main(args=None):
    rclpy.init(args=args)
    node = opasistidaNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()



