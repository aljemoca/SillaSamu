#!/usr/bin/env python3
# -*- coding: utf-8 -*-



"""

Created on Fri May 23 09:45:36 2025

@author: labserver
"""

import time
import datetime
import cv2 # Importamos OpenCV

class Webcam:
    def __init__(self):
        #self.intervalo = º.
        self.camera = cv2.VideoCapture(0,cv2.CAP_V4L2)  # Inicializa la webcam (0 es usualmente la cámara por defecto) 
        if not self.camera.isOpened():
            print("Error: No se pudo acceder a la cámara.")
            return 
    # Intenta forzar el formato MJPG
    # ⚠️ Intenta forzar la cámara a usar YUYV o YUY2
        #fourcc_yuyv = cv2.VideoWriter_fourcc('Y', 'U', 'Y', '2')
        fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
        self.camera.set(cv2.CAP_PROP_FOURCC, fourcc)
        # Opcional: Ajustar la resolución. No todas las cámaras soportan cualquier resolución.
      # Si 640x480 sigue fallando, prueba la resolución más pequeña:
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640) 
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480) 
        self.camera.set(cv2.CAP_PROP_FPS, 10)           # De 30 a 15 FPS
        time.sleep(2)
        self.ruta = "./fotos/"
        #elf.stop = 0
        self.n_frame = 1
        
    def tomar_foto(self):
        ret, frame = self.camera.read()  # Lee un fotograma de la cámara
        if not ret:
            print("Error: No se pudo leer el fotograma de la cámara.")
            return 0
        else:
            fecha_hora_actual = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            nombre = self.ruta + fecha_hora_actual +'_'+str(self.n_frame)+ '.jpg'
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            cv2.imwrite(nombre, frame_rgb)  # Guarda el fotograma como imagen
            self.n_frame+=1
            print(f"Foto guardada: {nombre}")
        return self.n_frame
    
    #def tomar_secuencia(self):
    #    self.stop = 0
    #    while not self.stop:
    #        time.sleep(self.intervalo)
    #        self.tomar_foto()
            
    def setRuta(self, ent):
        self.ruta = ent
        
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
