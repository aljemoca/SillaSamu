import rclpy
from rclpy.node import Node
from samuchair_interfaces.srv import ArduinoMotor
import time
class NodoCliente(Node):
    def __init__(self):
        super().__init__('nodo_cliente')
        self.cli = self.create_client(ArduinoMotor, 'control_joystick')

        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Esperando al servicio...')

        self.req = ArduinoMotor.Request()
  

    def enviar_peticion(self,a,b,c):
        
        self.req.command=a
        self.req.x =b
        self.req.y =c


        future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, future)
        return future.result()

           

def main():
    rclpy.init()
    cliente = NodoCliente()
    respuesta = cliente.enviar_peticion('modo',0,0)
    cliente.get_logger().info(f'Status: {respuesta.status}')
    cliente.get_logger().info('Respuesta:'+ respuesta.out)
    cliente.get_logger().info(f'x: {respuesta.x}')
    cliente.get_logger().info(f'y: {respuesta.y}')
    time.sleep(2)

    respuesta = cliente.enviar_peticion('modo',1,0)
    cliente.get_logger().info(f'Status: {respuesta.status}')
    cliente.get_logger().info('Respuesta:'+ respuesta.out)
    cliente.get_logger().info(f'x: {respuesta.x}')
    cliente.get_logger().info(f'y: {respuesta.y}')
    time.sleep(10)


    respuesta = cliente.enviar_peticion('modo?',1,0)
    cliente.get_logger().info(f'Status: {respuesta.status}')
    cliente.get_logger().info('Respuesta:'+ respuesta.out)
    cliente.get_logger().info(f'x: {respuesta.x}')
    cliente.get_logger().info(f'y: {respuesta.y}')
    time.sleep(2)

    respuesta = cliente.enviar_peticion('velocidad?',1,0)
    cliente.get_logger().info(f'Status: {respuesta.status}')
    cliente.get_logger().info('Respuesta:'+ respuesta.out)
    cliente.get_logger().info(f'x: {respuesta.x}')
    cliente.get_logger().info(f'y: {respuesta.y}')
    time.sleep(2)


    respuesta = cliente.enviar_peticion('velocidad',100,200)
    cliente.get_logger().info(f'Status: {respuesta.status}')
    cliente.get_logger().info('Respuesta:'+ respuesta.out)
    cliente.get_logger().info(f'x: {respuesta.x}')
    cliente.get_logger().info(f'y: {respuesta.y}')
    time.sleep(10)


    respuesta = cliente.enviar_peticion('velocidad?',1,0)
    cliente.get_logger().info(f'Status: {respuesta.status}')
    cliente.get_logger().info('Respuesta:'+ respuesta.out)
    cliente.get_logger().info(f'x: {respuesta.x}')
    cliente.get_logger().info(f'y: {respuesta.y}')
    time.sleep(2)

    respuesta = cliente.enviar_peticion('modo',0,0)
    cliente.get_logger().info(f'Status: {respuesta.status}')
    cliente.get_logger().info('Respuesta:'+ respuesta.out)
    cliente.get_logger().info(f'x: {respuesta.x}')
    cliente.get_logger().info(f'y: {respuesta.y}')
    time.sleep(2)



    rclpy.shutdown()

if __name__ == '__main__':
    main()