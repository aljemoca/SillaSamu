#!/usr/bin/env python3
# -*- coding: utf-8 -*-



"""

Created on Fri May 23 09:45:36 2025

@author: labserver
"""

import time
import datetime
import cv2 # Importamos OpenCV
from pathlib import Path 


class Webcam:
    def __init__(self):
        self.initiate()

    def initiate (self):
        #se comentan las 5 lineas de abajo
        #self.camera = cv2.VideoCapture(0,cv2.CAP_V4L2)  # Inicializa la webcam (0 es usualmente la cámara por defecto) 
        #self. testOpenCamera()
        #if not self.camera.isOpened():
        #    print("Error: No se pudo acceder a la cámara.")
         #   return 

    # Intenta forzar el formato MJPG
    # ⚠️ Intenta forzar la cámara a usar YUYV o YUY2
        #fourcc_yuyv = cv2.VideoWriter_fourcc('Y', 'U', 'Y', '2')

        #se comentan las 2 lineas de abajo
        #fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
        #self.camera.set(cv2.CAP_PROP_FOURCC, fourcc)

        # Opcional: Ajustar la resolución. No todas las cámaras soportan cualquier resolución.
      # Si 640x480 sigue fallando, prueba la resolución más pequeña:

        #se comentan las 3 lineas de abajo
        #self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640) 
        #self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480) 
        #self.camera.set(cv2.CAP_PROP_FPS, 10)           # De 30 a 15 FPS
        time.sleep(2)
        self.connected=None
        self.ruta = "./fotos/"   
        #elf.stop = 0
        self.n_frame = 1
        self.name=''
    
    def configureCamera(self):
        fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
        self.camera.set(cv2.CAP_PROP_FOURCC, fourcc)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640) 
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480) 
        self.camera.set(cv2.CAP_PROP_FPS, 10) 
        time.sleep(2)

    def connectCamera(self):
        if not self.connected:
            for i in range(5):
                self.camera = cv2.VideoCapture(i,cv2.CAP_V4L2)
                time.sleep(1)
                if self.camera.isOpened():
                    ret, _ =self.camera.read()
                    if ret:
                        print(f"cámara reconectada en {i}")
                        self.configureCamera()
                        self.connected = True
                        return True
                    else:
                        print("no hay ret")
                        self.camera.release()
                        self.connected = False
                        #return False
                else:
                    print("no se pudo conectar")
                    self.connected = False
                    #return False
            print("aqui en for")
            return False
        else:
            print("not self connected")
            return True 
                   
            
    def readFrame(self):
        #if not self.connected:
            if not self.camera or not self.camera.isOpened():
                if not self.connectCamera():
                    self.connected = False
                    return False
            ret, frame = self.camera.read()
            if not ret:
                self.connected = False
                print("camara desconectada")
                if not self.connectCamera():
                    print("no hay foto y no he conectado")
                    self.connected = False
                    return False
                else:
                    print("connect camera devuelve verdadero")
                    self.connected = True
                    return True
            else:
                print("hay foto")
                self.connected = True
                return True
        #else:
        #    return True
    def statusCamera (self):
        return self.connected

    def setName(self,name):
        self.name=name

    def tomar_foto(self):
        ret, frame = self.camera.read()  # Lee un fotograma de la cámara
        if not ret:
            #print("Error: No se pudo leer el fotograma de la cámara.")
            #return 0
            self.connected = False
            print("camara desconectada")
            if not self.connectCamera():
                print("no hay foto y no he conectado")
                self.connected = False
                return False
            else:
                print("connect camera devuelve verdadero")
                self.connected = True
                return True
        else:
            if self.name is not None:
                self.n_frame+=1
                fecha_hora_actual = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
                #nombre = self.ruta + self.name+'_'+fecha_hora_actual +'_'+str(self.n_frame)+ '.jpg'
                nombre = self.ruta +fecha_hora_actual +'_'+str(self.n_frame)+ '.jpg'
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                cv2.imwrite(nombre, frame_rgb)  # Guarda el fotograma como imagen
                print(f"Foto guardada: {nombre}")
        return self.connected, self.n_frame
    def frameZero (self):
        self.n_frame = 0

    #def tomar_secuencia(self):
    #    self.stop = 0
    #    while not self.stop:
    #        time.sleep(self.intervalo)
    #        self.tomar_foto()
            
    def setRuta(self, ent):
        self.ruta = './fotos/'+ent+'/'
        ruta = Path(self.ruta)
        ruta.mkdir(parents=True,exist_ok=True)

    #def setTs(self, Ts):
    #    self.intervalo = Ts
    
    #def getTs(self):
    #        return self.intervalo
        
    def parar(self):
        #self.stop = 1
        self.camera.release() # Libera la cámara cuando terminamos
        cv2.destroyAllWindows()




##################### PROGRAMA DE PRUEBA ################################333333
#cap = cv2.VideoCapture(0,cv2.CAP_V4L2)

#if not cap.isOpened():
#    print("❌ No se pudo abrir la cámara.")
    
    
#print("✅ Cámara iniciada. Esperando frames...")

#while True:
#    ret, frame = cap.read()

#    if not ret:
#        print("⚠️ No se recibió ningún frame. Esperando 1 segundo...")
#        time.sleep(1)
#        continue  # o haz break si quieres salir

#    cv2.imshow("Vista cámara", frame)

#    if cv2.waitKey(1) & 0xFF == ord('q'):
#        break

#cap.release()
#cv2.destroyAllWindows()
