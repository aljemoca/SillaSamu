import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Bool
import subprocess
import signal
import os
from datetime import datetime
from pathlib import Path

class BagControlNode(Node):
    def __init__(self):
        super().__init__('bag_control_node')
        self.nombre = None
        # Suscriptor para activar/desactivar (True = Grabar, False = Parar)
        self.subscription = self.create_subscription(
            Bool,
            'control_grabacion',
            self.control_callback,
            10)
        
        self.nombre_topic = self.create_subscription(
            String,
            'directorio_grabacion', 
            self.nombre_callback,
            10)
        self.bag_process = None
        self.get_logger().info('Nodo de Control de Grabación Operativo.')
        

    def control_callback(self, msg):
        if msg.data:
            self.start_bag()
        else:
            self.stop_bag()

    def nombre_callback(self,msg):
        self.nombre = './samuchair_bag/'
        self.nombre = self.nombre + msg.data 
        self.get_logger().info(f'Nombre seleccionado: {self.nombre}')
 

    def start_bag(self):
        if self.bag_process is None and self.nombre is not None:
            # Generamos un nombre único basado en la fecha y hora
            #timestamp = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
            bag_name = self.nombre #+ f"_{timestamp}"
            #bag_name =  'sesion' + f"_{timestamp}"
            

            # Comando: ajusta los tópicos que realmente necesites
            cmd = [
                "ros2", "bag", "record", "-a",
                "-o", bag_name
            ]
            
            # preexec_fn=os.setsid es vital para poder matar el proceso correctamente luego
            self.bag_process = subprocess.Popen(cmd, preexec_fn=os.setsid)
            self.get_logger().info(f'Iniciando grabación: {bag_name}')
        else:
            self.get_logger().warn('Ya hay una grabación en curso o nombre de directorio incorrecto.')

    def stop_bag(self):
        if self.bag_process:
            # Enviamos SIGINT al grupo de procesos (esto cierra el YAML correctamente)
            os.killpg(os.getpgid(self.bag_process.pid), signal.SIGINT)
            self.bag_process.wait()
            self.bag_process = None
            self.get_logger().info('Grabación finalizada y metadatos guardados.')
        else:
            self.get_logger().warn('No hay ninguna grabación activa para detener.')

def main(args=None):
    rclpy.init(args=args)
    node = BagControlNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()