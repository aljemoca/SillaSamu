import rclpy
from rclpy.node import Node
import serial
import time

from samuchair_interfaces.srv import ArduinoMotor  # Importa tu srv generado

from samuchair import ComJoystickManual


class arduinoNode(Node):

    def __init__(self):
        super().__init__('motor_service')
        self.arduino = ComJoystickManual.ComJoystickManual()  # Ajusta el puerto según corresponda
        # Crea el servicio
        self.srv = self.create_service(ArduinoMotor, 'control_joystick', self.handle_joystick_silla)


        # Inicializa conexión serial con Arduino
        try:
            puerto = '/dev/Joystick'     #Tiene que estar en las reglas udev
            self.arduino.establecePuerto(puerto)
            self.get_logger().info("Conectado al Arduino por "+puerto)
            #Puede ser modo local (1: el usuario usa joystick) o modo remoto 1
            if self.arduino.esLocal():
                self.modo=0
            else:
                self.modo=1
            self.timer = self.create_timer(6.0, self.timer_callback)  # Llama a la función cada segundo

        except:
            self.get_logger().error(f"No se pudo abrir el puerto serie")
        
    def timer_callback(self):
        if self.modo==1:    #En modo remoto se manda cada 6 segundos comandos para que no pase a modo local
            if self.arduino.esLocal():  #Me da mal rollo que pueda haber varios procesos accediendo al puerto. Pensar bloquearlos
                self.modo=0

    def __del__(self):
        self.arduino.close()
        del self.arduino

    def handle_joystick_silla(self, request, response):
        if not self.arduino.conectado():
            response.success = False
            response.out = "Puerto serie no disponible"
            return response

        command = request.command.strip()
        self.get_logger().info(f"Enviando comando al Arduino: {command}")
        print(command)

        
        if command == 'modo':
            if request.x == 0:
                response.status=self.arduino.controlLocal();
                response.out='Configurando Local'
                if response.status:
                    self.modo=0
            else:
                response.status=self.arduino.controlRemoto();
                response.out='Configurando Remoto'
                if response.status:
                    self.modo=1

        if  command == 'modo?':
            response.status = True
            response.x = self.modo  
            if response.x == 0:
                response.out = 'Usuario'
            else:
                response.out = 'Cuidador'              
            
        if command == 'velocidad':
            response.status=self.arduino.escribeMandos(request.x,request.y)
            response.out='Configurando Velocidad'    
        if command == 'velocidad?':
            response.status,response.x,response.y=self.arduino.consultaXY()
            response.out='Consulta velocidad'
        return response


def main(args=None):
    rclpy.init(args=args)
    node = arduinoNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        del node
        rclpy.shutdown()


if __name__ == '__main__':
    main()
