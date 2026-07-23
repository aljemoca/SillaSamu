import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from samuchair import gpioRaspberry
import time

ledVerde = 20
ledAzul = 21

class alarmNode (Node):
    def __init__(self):
        super().__init__('alarmNode')
        #Mapeo de estados de los nodos
        self.statusNode = {
            'esp32Node': None,
            'movilNode': None,
            'secondarytaskNode': None,
            'arduinoNode': None,
            'webcamNode': None
        }
        #instanciamos la clase
        self.ledVerde = gpioRaspberry.Puerto()
        self.ledAzul = gpioRaspberry.Puerto()
        self.ledVerde.pinModeOut(ledVerde)
        self.ledAzul.pinModeOut(ledAzul)

        #suscripciones a los topics
        self.create_subscription(String, 'esp32_status',self.esp32Callback, 10)
        self.create_subscription(String, 'Movil_status',self.movilCallback, 10)
        self.create_subscription(String, 'Headphones_status',self.headphoneCallback, 10)
        self.create_subscription(String, 'arduino_status',self.arduinoCallback, 10)
        self.create_subscription(String, 'webcam_status',self.webcamCallback, 10)

        #timer máquina de estados
        self.tick = False
        self.create_timer(0.5, self.timer_led)

    #callback suscriptores
    def esp32Callback (self, msg):
        status = msg.data

        if status == 'CONNECTED':
            self.statusNode['esp32Node'] = True
        elif status == 'DISCONNECTED':
            self.statusNode['esp32Node'] = False
            self.get_logger().error("No hay conexión con el ESP32")

    def movilCallback (self, msg):
        status = msg.data

        if status == 'CONNECTED':
            self.statusNode['movilNode'] = True
        elif status == 'DISCONNECTED':
            self.statusNode['movilNode'] = False
            self.get_logger().error("No hay conexión con el puerto serie bluetooth que gestiona el móvil")

    def headphoneCallback (self, msg):
        status = msg.data

        if status == 'CONNECTED':
            self.statusNode['secondarytaskNode'] = True
        elif status == 'DISCONNECTED':
            self.statusNode['secondarytaskNode'] = False
            self.get_logger().error("No hay conexión con el auricular")

    def arduinoCallback (self, msg):
        status = msg.data

        if status == 'CONNECTED':
            self.statusNode['arduinoNode'] = True
        elif status == 'DISCONNECTED':
            self.statusNode['arduinoNode'] = False
            self.get_logger().error("No hay conexión con el Arduino")
    
    def webcamCallback (self, msg):
        status = msg.data

        if status == 'CONNECTED':
            self.statusNode['webcamNode'] = True
        elif status == 'DISCONNECTED':
            self.statusNode['webcamNode'] = False
            self.get_logger().error("No hay conexión con la webCam")
    
    
    #controlLeds
    def timer_led( self ):
        self.tick = not self.tick
        if self.statusNode['secondarytaskNode'] == False:
            self.ledAzul.digitalWrite(1)
            self.ledVerde.digitalWrite(1)
            return
        
        if self.statusNode['webcamNode'] == False:
            self.ledVerde.digitalWrite(self.tick)
            self.ledAzul.digitalWrite(self.tick)
            return

        if self.statusNode['arduinoNode'] == False:
            self.ledAzul.digitalWrite(self.tick)
            self.ledVerde.digitalWrite( not self.tick)
            return
        
        if self.statusNode['esp32Node'] == False or self.statusNode['movilNode'] == False:
            if self.statusNode['esp32Node'] == False:
                self.ledVerde.digitalWrite(self.tick)
            else:
                self.ledVerde.digitalWrite( 0 )
            if self.statusNode['movilNode'] == False:
                self.ledAzul.digitalWrite(self.tick)
            else:
                self.ledAzul.digitalWrite( 0 )
            return

        
        self.ledAzul.digitalWrite(0)
        self.ledVerde.digitalWrite(0)

def main(args=None):
    rclpy.init(args=args)
    node = alarmNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        # Apagar LEDs por seguridad al salir
        node.ledAzul.digitalWrite(0)
        node.ledVerde.digitalWrite(0)
        pass
    finally:
        #node.destroy_node()
        
        rclpy.shutdown()

if __name__ == '__main__':
    main()