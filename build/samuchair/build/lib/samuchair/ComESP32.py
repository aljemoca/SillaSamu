# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""



import serial
from time import sleep

import rclpy
from rclpy.node import Node
from std_msgs.msg import String  

class ComESP32:
    """Comunicación con la STM32"""
    
    def __init__(self,port="/dev/ttyUSB0"):
        self.data = [0,0,0,0,0,0,0,0]    
        #self.ser = serial.Serial("/dev/ttyS0",baudrate=115200,timeout=0.5)
        self.ser = serial.Serial(port,baudrate=115200,timeout=0.5)
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
        #print(self.data)
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
