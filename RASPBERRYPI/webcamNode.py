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
#from samuchair_interfaces.srv import Movil 

class webcamNode(Node):
    def __init__(self):
        super().__init__('webcam_node')
        self.webcam = Webcam.Webcam()  # Ajusta el puerto según corresponda
        self.publisher_frame = self.create_publisher(Int32, 'frame', 10)
        self.timer = self.create_timer(2, self.timer_callback)  # Llama a la función cada segundo
        #self.timerReconnect = self.create_timer(2, self.webCam_reconnect)
#        self.cliente = self.create_client(Movil, 'sujeto_experimental')  #Se añade este cliente para obtener el nombre del sujeto
        self.activa_webcam = False
#        while not self.cliente.wait_for_service(timeout_sec=1.0):
#            self.get_logger().info('Esperando al servicio para el nombre del sujeto...')
#        self.req = Movil.Request()
#        self.request_subject_name_and_setup()
        self.subscription1 = self.create_subscription(String,'name_movil',self.sus_name_movil,4)
        self.subscription2 = self.create_subscription(Int32,'Ejecucion',self.sus_ejecucion,4)
        self.name = ''


    def __del__(self):
        """Asegura que la cámara se cierre cuando el objeto es destruido."""
        if hasattr(self, 'webcam') and self.webcam.isOpened():
            self.destroy_webcam()
            print("Cámara liberada por el destructor.")
        super().destroy_node()

    def sus_name_movil(self,msg):
        self.name = msg.data
        self.webcam.setName(self.name)

    def sus_ejecucion(self,msg):
        if msg.data == 20:   #Mensaje Go!
            self.activa_webcam=True
        elif msg.data == 30:  #Mensaje Stop!
            self.activa_webcam=False
            


    def timer_callback(self):
        if self.activa_webcam:
            frame = self.webcam.tomar_foto()
            msg = Int32()
            msg.data = int(frame)
            self.publisher_frame.publish(msg)
            self.get_logger().info(f'Frame: {msg.data}')
            # if frame == 0:
            #     self.destroy_webcam()
            #     self.webcam.iniate()
    
    def webCam_reconnect(self):
        pass 


    # def request_subject_name_and_setup(self):
    #     """
    #     Lanza la petición al servidor y asigna un callback al future.
    #     """
    #     if not self.cliente.wait_for_service(timeout_sec=1.0):
    #         self.get_logger().error('Servicio "sujeto_experimental" no disponible al inicio. Reintentando...')
    #         # Si el servicio no está listo, puedes usar otro timer para reintentar la llamada.
    #         # Por simplicidad aquí asumimos que en algún momento estará listo.
    #         return
        
    #     self.get_logger().info('Lanzando petición asíncrona por el nombre del sujeto.')
    #     self.req.command=1
    #     # 1. Llamada asíncrona
    #     future = self.cliente.call_async(self.req)
        
    #     # 2. Asignar un callback al future. Cuando la respuesta llegue, se ejecutará el método.
    #     future.add_done_callback(self.subject_name_response_callback)


    # def subject_name_response_callback(self, future):
    #     """
    #     Callback que se ejecuta automáticamente cuando la respuesta del servidor llega.
    #     """
    #     try:
    #         response = future.result()
    #         if response is not None:
    #             # Asumimos que la respuesta tiene un campo 'name'
    #             if response.status==True:
    #                 self.subject_name = response.name 
    #                 self.activa_webcam = True
    #                 self.webcam.setName(self.subject_name)
    #                 self.get_logger().info(f'🎉 Nombre obtenido: {self.subject_name}. Webcam activada.')
    #         else:
    #             self.get_logger().error('La llamada al servicio falló (respuesta vacía).')
    #     except Exception as e:
    #         self.get_logger().error(f'Excepción al procesar la respuesta: {e}')



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
