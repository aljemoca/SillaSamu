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


import serial
from time import sleep

class ComESP32:
    """Comunicación con la STM32"""
    
    def __init__(self):
        self.data = [0,0,0,0,0,0,0,0]    
        #self.ser = serial.Serial("/dev/ttyS0",baudrate=115200,timeout=0.5)
        self.ser = serial.Serial("/dev/ttyUSB0",baudrate=115200,timeout=0.5)
        self.rx_flag=0
    

    def send(self,comando):
        self.ser.write(comando)
        sleep(0.1)
        return
        
    def conectado(self):  #Comprobar
        comando=b'\x01'
        error=False
        self.send(comando)
        self.data[0] =self.ser.read()
        if self.data[0]!=b'\x01':
            error=True
        print(self.data)
        return not error
    
    def	comandoMedidas(self): #Comprobar
        comando=b'\x34'
        self.send(comando)
        return self.esperaRespuesta()


        
    #Esta función de abajo hay que paralelizarla
    #se puede seguir la misma idea que en el STM32
    #activando un flag y ponerla en un hilo aparte
    def esperaRespuesta(self):  #Comprobar esta funcion
        error=False
        cont = 0
        self.data = [0,0,0,0,0,0,0,0] 
        while cont<8:
            self.data[cont] =self.ser.read()
            cont+=1 
         #   if self.data[0]==b'\x01':
         #       cont=6
         #       error = True
        if self.data[0]!=b'\xaa' and cont>0:
            error=True
        print(self.data)
        return error
    
    
    def obtenerMedidas(self):
        error= self.comandoMedidas();
        pot = 0;
        giro = [0,0]
        hall= [0,0]

        pot = int(self.data[1].hex(),16)
        giro[0] = int(self.data[2].hex(),16)
        hall[0] = int(self.data[3].hex(),16) <<8 
        hall[0] += int(self.data[4].hex(),16)  #ver si esto va bien
        giro[1] = int(self.data[5].hex(),16)
 
        hall[1] = int(self.data[6].hex(),16) <<8 
        hall[1] += int(self.data[7].hex(),16)  #ver si esto va bien
      
        res = list([error,pot,giro,hall])
        return  res





class esp32Node(Node):
    def __init__(self):
        super().__init__('esp32_node')
        self.esp32 = ComESP32()  # Ajusta el puerto según corresponda
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
