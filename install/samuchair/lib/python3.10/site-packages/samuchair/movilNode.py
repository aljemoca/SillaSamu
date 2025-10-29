
import rclpy
from rclpy.node import Node
from std_msgs.msg import String  # Ajusta el tipo de mensaje según tus necesidades
from std_msgs.msg import Int32
 # Asegúrate de que la ruta de importación sea correcta
import serial
from time import sleep


#Comunicaciones con el Móvil
#Este nodo hace de puente entre el puerto serie que se conecta con el móvil, el cual recibe
#la información del sujeto (su nombre) y los comandos que definen el comienzo y el fin de #cada etapa del circuito de pruebas.
#Todos los comandos que se reciben se publican
#Los comandos tienen el siguiente formato:
#
#       Nombre!   Si la longiud de lo recibido es mayor de dos, se considera el nombre del sujeto
#       G!  Indica que comienza el experimento
#       S!  Indica que el experimento ha acabado
#       Fx!  Marcamos una fase   x=0,1,2,......E!
#       Tx! Seleccionamos el tipo x=0,1
#       Mx!  Seleccionamos modo de operación x=0,1,2
#       E! Señalizar fase errónea
#       Q! Señalizar fin de la fase



class ComMovil:
    
    def __init__(self):
        self.puerto=''
        self.ser=''
        self.comandoRecibido=False
        self.buffer=['0']*30
        self.comando=''
        self.index=0
        return
    
    def isCommandReady(self):
        return self.commandoRecibido
    
    def __del__(self):
        self.ser.close()

    def	conectado(self):
        ok=True
        if self.puerto=='':
            ok=False
        return ok  
   

    def hayDatos(self):
        return self.ser.in_waiting>0
    

    def hayComando(self):
        while self.hayDatos() and not self.comandoRecibido:
            self.buffer[self.index]=self.ser.read().decode()
            if self.buffer[self.index]=='!':
                self.comando=''.join(self.buffer[0:self.index])
                self.comandoRecibido=True
                self.index=0
                print(f'Comando: {self.buffer}')
            else:
                if self.buffer[self.index]!='\r' and self.buffer[self.index]!='\n':
                    self.index = self.index+1
                self.commandoRecibido=False
        return self.comandoRecibido
    
    def lecturaComando(self):
        res = self.comando
        self.comando=''
        self.comandoRecibido=False
        self.index=0
        return res
    
    def commandParser(self,ent):
        #print(ent)
        if len(ent)>2:
            tipo,valor=1,ent
        else:
            ent[0] = ent[0].upper()
            if ent[0]=='G':
                tipo,valor=2,''
            elif ent[0]=='S':
                tipo,valor=3,''
            elif ent[0]=='E':
                tipo,valor=6,''
            elif ent[0]=='F':
                tipo,valor=4,ent[1]
            elif ent[0]=='T':
                tipo,valor=5,ent[1]
            elif ent[0]=='M':
                tipo,valor=7,ent[1]
            elif ent[0]=='Q':
                tipo.valor=8,ent[1]
            else:
                tipo=-1
                valor='0'
        return tipo,valor


    
    def	buscaPuerto(self):
        raiz='/dev/ttyUSB'
        mensaje="Buscando puerto para el control del motor"
        sleep(2.0)
        print(mensaje)
        ok=False
        for p in range(4):
            portname=raiz+str(p)
            ser=[]
            if(self.establecePuerto(portname)):
                ok=True;
                return ok
        return ok
 
            
    def consultaPuerto(self):
        return self.puerto
    
    def establecePuerto(self,puerto):
        ok=False
        cont=0
        print(puerto)
        try:
            self.ser=serial.Serial(port=puerto, baudrate=9600,timeout=0.5)
            #print(self.ser)
            sleep(2.0)
        except:
                #print("No hay puerto"+portname)
            print('No fue posible la conexión al puerto '+ puerto)


        return ok
    


class movilNode(Node):
    def __init__(self):
        super().__init__('movil_node')
#        self.port = "/dev/Joystick"
        self.port = "/dev/ttyUSB0"
        self.movil = ComMovil()  # Ajusta el puerto según corresponda
        self.movil.establecePuerto(self.port)
        self.publisher_name = self.create_publisher(String, 'name_movil', 2)
        self.publisher_tipo = self.create_publisher(String,'tipo_exp',2)
        self.publisher_modo = self.create_publisher(String,'modo_exp',2)
        self.publisher_ejecucion = self.create_publisher(Int32,'Ejecucion',5)
        self.timer = self.create_timer(0.5, self.timer_callback)  # Llama a la función cada segundo


    def timer_callback(self):
        if self.movil.hayComando():
            comando=self.movil.lecturaComando()
            print(comando)
            tipo,valor=self.movil.commandParser(comando)
            print(f'tipo: {tipo}')
            if tipo==1:
                msg = String()
                msg.data = valor
                self.publisher_name.publish(msg)
                self.get_logger().info(f'Dato publicado Nombre_Sujeto: {msg.data}')
            elif tipo==5:
                msg = String()
                msg.data = 'Experimento '+valor
                self.publisher_tipo.publish(msg)
                self.get_logger().info(f'Dato publicado Tipo Experimento: {msg.data}')
            elif tipo==7:
                msg =String()
                msg.data = 'Modo:'+valor
                self.publisher_modo.publish(msg)
                self.get_logger().info(f'Dato publicado Modo: {msg.data}')
            else:
                msg = Int32()
                if tipo==2:
                    msg.data = 20  #Start
                elif tipo==3:
                    msg.data = 30 #Stop
                elif tipo==6:
                    msg.data=40   #Error
                elif tipo==4:
                    msg.data=int(valor,16)
                elif tipo==8:
                    msg.data=50
                else:
                    msg.data = -1
                self.publisher_ejecucion.publish(msg)
                self.get_logger().info(f'Dato publicado Fase Ejecucion: {msg.data}')
            

    def destroy_serial(self):
        del self.movil

def main(args=None):
    rclpy.init(args=args)
    node = movilNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_serial()  # Asegúrate de cerrar la conexión serial
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
