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

#from SecondaryTask import SecondaryTask




import sounddevice as sd 
import numpy as np
#import threading
import time
#import matplotlib.pyplot as plt


class SecondaryTask:
    def __init__(self):
        self.intervalo = np.array(np.array([5,10],dtype='float'))
        self.Fs = 8000
        #self.data = [0]
        self.flanco=1
        self.contframes=0
        self.wave = self.buildTone()
        self.semaforo = False
        #Cada tono se genera de media unos 20 segundos con una 
        #variabilidad de 5 segundos
        try:
            self.audiostream= sd.InputStream(
                callback=self._audio_callback,
                channels=1,
                samplerate=self.Fs
                )
            self.audiostream.start()
            print('Se ha iniciado la captura de audio')            
        except:
            print('No se puede iniciar la captura de audio')
    
    def buildTone(self,duration=0.5):
        F = 440
        N = int(duration*self.Fs)
        n = np.arange(N)
        f = F/self.Fs
        wave = 2*np.sin(2*np.pi*f*n)
        return wave
        
    def playTone(self):
        sd.play(self.wave, samplerate=self.Fs, blocking=False)
        self.tiempo=0
        self.contframes=0
        self.flanco=0
        

    def setFs(self,Fs):
        self.Fs = Fs
    
    def setTimeInterval(self,intervalo):
        self.intervalo = intervalo
    
    def nextTimePoint(self):
        return  self.intervalo[0] + self.intervalo[1]*np.random.rand()


    def _audiocallback(self, indata, frames,time,status ):
        self.maxFrame(indata,frames,time,status)



    def maxFrame(self, indata, frames, time, status):
        data=np.max(indata)
        if self.flanco==0:
            if  data >0.005:
                pos = np.where(indata[:,0] == data)[0]
                self.flanco=1
                self.tiempo = (self.contframes + pos[0] )/self.Fs
                print(f"Tiempo={self.tiempo}")
            else:
                self.contframes+=frames
                
        else:
            self.contframes=0
        
    def dataReady(self):
        return self.semaforo
    
    def readTime(self):
        self.semaforo=False
        return self.tiempo
    
    
    def stop(self):
        self.audiostream.stop()
        
    def start(self):
        self.audiostream.start()
        
        





class secondarytaskNode(Node):
    def __init__(self):
        super().__init__('st_node')
        self.st = SecondaryTask()  
        self.publisher_st_nexttime = self.create_publisher(Float32, 'random_time', 10)
        self.publisher_st_medida = self.create_publisher(Float32,'diff_time',10)
        self.interval = self.st.nextTimePoint()
        self.timer = self.create_timer(1.0,self.timer_callback)
        self.tiempo_inicio = self.get_clock().now()
        self.publish_loop()
        #self.timer = self.create_timer(1.5, self.timer_callback)  # Llama a la función cada segundo

    def start_random_timer(self):
        self.interval = self.st.nextTimePoint()
        if self.timer:
            self.timer.cancel()
        self.timer = self.create_timer(self.interval,self.timer_callback)
        self.tiempo_inicio = self.get_clock().now()
        
    def timer_callback(self):      
        msg = Float32()
        msg.data = self.interval
        self.publisher_st_nexttime.publish(msg)
        self.get_logger().info(f'Dato publicado ST: {msg.data}')
        duration = (self.get_clock().now()-self.tiempo_inicio).nanoseconds/1000000000.0
        msg.data = duration
        self.publisher_st_medida.publish(msg)
        self.get_logger().info(f'Dato publicado ST Medida: {msg.data}')
        self.st.playTone()        
        self.start_random_timer()

    def publish_loop(self):
        msg_count = 0
        while rclpy.ok():
            #delay = self.st.nextTimePoint();
            msg = Float32()
            if st.dataReady():
                msg.data = st.readTime()
            self.publisher_st_medida.publish(msg)
            self.get_logger().info(f'Publicado: "{msg.data}"')


def main(args=None):
    rclpy.init(args=args)
    node = secondarytaskNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        #node.destroy_webcam()  
        rclpy.shutdown()

if __name__ == '__main__':
    main()
