#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 23 11:07:26 2025

@author: labserver
"""


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
        self.flanco=0
        self.contframes=0
        self.semaforo=True
        #Cada tono se genera de media unos 20 segundos con una 
        #variabilidad de 5 segundos
    def playTone(self,duration=0.5):
        F = 440
        N = int(duration*self.Fs)
        n = np.arange(N)
        f = F/self.Fs
        wave = 2*np.sin(2*np.pi*f*n)
        sd.play(wave, samplerate=self.Fs, blocking=True)
        sd.sleep(int(duration*1000))
    
    def setTimeInterval(self,intervalo):
        self.intervalo = intervalo
    
    def nextTimePoint(self):
        return  self.intervalo[0] + self.intervalo[1]*np.random.rand()

    def maxFrame(self,indata, frames, time, status):
        data=np.max(indata)
        if self.flanco==0:
            self.contframes=self.contframes+1
            if  data >0.005:
                self.flanco=1
                tiempo = self.contframes*len(indata)/self.Fs
                print(f"Tiempo={tiempo}")
        else:
            self.contframes=0
        #self.data.append(np.max(indata))
        print(data)
   
    def readData(self):
        return self.data
    
    def stop(self):
        self.semaforo=False
    
    def start(self):
        self.semaforo=True
        
        
    def run(self):
        self.semaforo=True
        cont=0
        while self.semaforo:
            t = self.nextTimePoint()
            print(t)
            time.sleep(t)
            self.playTone()
            self.flanco=0
            self.contframes=0
            cont+=1
            with sd.InputStream(callback=self.maxFrame, channels=1, samplerate=self.Fs):
                sd.sleep(int(2*1000))
        #plt.plot(self.data)
        #self.data=[]
