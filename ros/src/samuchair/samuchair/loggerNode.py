
import time
import os
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32, String, Float32, Bool
 # Asegúrate de que la ruta de importación sea correcta
import math
from datetime import datetime
import csv  
from pathlib import Path


class  loggerNode(Node):
    def __init__(self):
        super().__init__('mainNode')

        self.subJoy = self.create_subscription(Int32, "jBnode", self.callback_subJoy, 10)
        self.subMovilName = self.create_subscription(String,"name_movil", self.callback_subMovilName,10)     #Creo subscripción al nombre para ROS2BAG
        self.subMovilTipo = self.create_subscription(Int32, "tipo_exp_int", self.callback_subMovilTipo, 10)
        self.subMovilModo = self.create_subscription(Int32, "modo_exp_int", self.callback_subMovilModo, 10)
        self.subMovilEjecucion = self.create_subscription(Int32, "Ejecucion", self.callback_subMovilEjecucion, 10)
        self.subOpasistida = self.create_subscription(Int32, "op_manual_asistida", self.callback_subOpasistida, 10)
        self.grab = self.create_subscription(Bool, 'control_grabacion', self.callback_grab, 10)
        self.nombre_grab = self.create_subscription(String,'directorio_grabacion',self.callback_nombre_grab,10)
        self.webcam_frame = self.create_subscription(Int32, 'frame',self.callback_webcam,10)
        self.tactil_izq = self.create_subscription(Int32, 'tactil_izq',self.callback_tactil_izq, 10)
        self.tactil_der = self.create_subscription(Int32,'tactil_der',self.callback_tactil_der,10)
        self.st_nexttime = self.create_subscription(Int32, 'random_time',self.callback_random_time,  10)  #Se ha cambiado a enteros en ms
        self.st_medida = self.create_subscription(Int32,'diff_time',self.callback_diff_time,10)   #Se ha cambiado a tipo entero expresado en ms
        self.st_atendido = self.create_subscription(Int32,'Attended',self.callback_attended,10)
        self.pot = self.create_subscription(Int32, 'pot_esp32',self.callback_pot, 10)
        self.leftwheel = self.create_subscription(Int32,'left_wheel_steps',self.callback_left_wheel,10)
        self.rightwheel = self.create_subscription(Int32,'right_wheel_steps',self.callback_right_wheel,10)

        self.timer = self.create_timer(30,self.callback_timer)

        self.csv_name = datetime.now().strftime("./logger/log_%Y%m%d_%H%M%S.csv")
        self.csv_file = open( Path(self.csv_name),  'w', newline='', encoding='utf-8-sig')

        self.writer = csv.writer(self.csv_file,delimiter=';')

        self.writer.writerow([
            'timestamp_s',
            'topic',
            'value'
        ])
        self.get_logger().info('Nodo de logger activo')

        self.grab_encurso = False   #Identifica si una grabación está o no en curso (sin uso)

    def write_row(self, topic, value):

        now = self.get_clock().now()

        timestamp_ns = now.nanoseconds
        timestamp_s = str(timestamp_ns / 1e9)

        self.writer.writerow([
            timestamp_s,
            topic,
            str(value)
        ])

        self.csv_file.flush()


    def callback_timer(self):
        self.csv_file.flush()
        size_mb = os.path.getsize(self.csv_name) / (1024 * 1024)

        if size_mb > 0.05:   #Está pensado para 1MB cambiar 0.01 por 1
            
            self.csv_file.close()

            self.csv_name = datetime.now().strftime("./logger/log_%Y%m%d_%H%M%S.csv")
            self.csv_file = open( Path(self.csv_name),  'w', newline='', encoding='utf-8-sig')

            self.writer = csv.writer(self.csv_file,delimiter=';')

            self.writer.writerow([
                'timestamp_s',
                'topic',
                'value'
            ])
             
        

    def callback_subJoy(self,indata):
        self.write_row('jBnode',str(indata.data))
    def callback_subMovilName(self,indata):
        self.write_row('name_movil',indata.data)
    def callback_subMovilTipo(self,indata):
        self.write_row('tipo_exp',str(indata.data))
    def callback_subMovilModo(self,indata):
        self.write_row('modo_exp',str(indata.data))
    def callback_subMovilEjecucion(self,indata):
        self.write_row('Ejecucion',str(indata.data))
    def callback_subOpasistida(self,indata):
        self.write_row('op_manual_asistida',str(indata.data))    
    def callback_grab(self,indata):
        self.write_row('control_grabacion',str(indata.data))
    def callback_nombre_grab(self,indata):
        self.write_row('directorio_grabacion',(indata.data))
    def callback_webcam(self,indata):
        self.write_row('frame',str(indata.data))
    def callback_tactil_izq(self,indata):
        self.write_row('tactil_izq',str(indata.data))
    def callback_tactil_der(self,indata):
        self.write_row('tactil_der',str(indata.data))
    def callback_random_time(self,indata):
        self.write_row('random_time',str(indata.data))
    def callback_diff_time(self,indata):
        self.write_row('diff_time',str(indata.data))
    def callback_attended(self,indata):
        self.write_row('Attended',str(indata.data))
    def callback_pot(self,indata):
        self.write_row('pot_esp32',str(indata.data))
    def callback_left_wheel(self,indata):
        self.write_row('left_wheel_steps',str(indata.data))
    def callback_right_wheel(self,indata):
        self.write_row('right_wheel_steps',str(indata.data))



    def __del__(self):
        try:
            self.csv_file.flush()
            self.csv_file.close()
        except:
            pass


def main(args=None):
    rclpy.init(args=args)
    node = loggerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        rclpy.shutdown()

if __name__ == '__main__':
    main()
