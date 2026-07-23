#import evdev
from evdev import InputDevice, categorize, ecodes, list_devices
import threading
import serial
import time


#creates object 'gamepad' to store the data
#you can call it whatever you lik
#gamepad = InputDevice('/dev/input/event2')

#prints out device info at start


btA = 304 #boton B
btB = 305 #boton D
btY = 308 #boton A
btX = 307 #boton C
btR = 311 #boton SpeedUp
btL = 310 #boton SpeedDown
btR2 = 313
btL2 = 312
Xaxys = 1
Yaxys = 1
Xcode = 1
Ycode = 1
m = 0
Yaxys_mem1 = 1
Xaxys_mem1 = 1
Yaxys_mem2 = 1
Xaxys_mem2 = 1

class ComJoyBluetooth:
    def __init__(self):
        self.bluetoothConnected = False
        self.gamepad = None
        """ try:
            self.ser = serial.Serial("/dev/ttyProlific0", baudrate = 9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)
        except:
            print("No existe el dispositivo Prolific0") """
        self.stop_event = threading.Event()
        #print(self.gamepad)
        #print(self.ser)
        self.command = 0
        self.flag = 0
        self.Xcode = 0
        self.Ycode = 0
        self.Ycruccode = 0
        self.Xcruccode = 0
        self._funcion = None
        self.joyBlueRun = threading.Thread(target=self.run)
        self.joyBlueRun.start()

        self.XY = None

    def _find_magicSee(self):
            for path in list_devices():
                device = InputDevice(path)
                print(device)
                name  = device.name.strip()
                if "8Bitdo SF30 Pro" in name:
                    #self.gamepad = InputDevice('/dev/input/event6')
                    self.bluetoothConnected = True
                    #self.joyBlueRun = threading.Thread(target=self.run)
                    #self.joyBlueRun.start()
                    #self.joyBlueRun.daemon = True
                    self.gamepad = device
                    print(self.gamepad)
                    return self.gamepad
                        
#         try:
#             
#             self.joyBlueRun = threading.Thread(target=self.run)
#             #self.joyBlueRun.daemon = True
#         except:
#             print("No se puede crear hilo no hay dispositivo Joystick Bluetooth")
            
    def __del__(self):
         print ("Object gets destroyed")
         del self.gamepad
         
    def consultaFlag(self):
        return self.flag
    
    def consultacommando (self):
        self.flag = 0
        return self.command
    
    def reiniciaHilo (self):
        try:
            self.joyBlueRun = threading.Thread(target=self.run)
            self.joyBlueRun.start()
            
        except:
            print("no Se ha podido reiniciar el Hilo")
           
        return self.joyBlueRun.is_alive()
    
    def consultaConexion (self):
        return self.bluetoothConnected
    
    def consultaHilo (self):
        return self.joyBlueRun.is_alive()
    
    def iniciaConexion (self):
        try:
            self.gamepad = InputDevice('/dev/input/event6')
            self.bluetoothConnected = True
            #print(gamepad)
        except:
            print("No hay dispositivo Joystick Bluetooth")
            self.bluetoothConnected = False
            #print(gamepad)
        return self.bluetoothConnected
    
    def set_callback (self, funcion):
        self._funcion = funcion
        
    def stop(self):
        """Detiene el hilo de forma segura."""
        self.stop_event.set()
        self.thread.join()
        #print("Hilo detenido y clase finalizada.")
    
    def run (self):
           
        """Hilo principal que maneja la conexión y lectura de eventos."""
        while not self.stop_event.is_set():
            if not self.gamepad:
                self.gamepad = self._find_magicSee()
                if not self.gamepad:
                    print("Gamepad no encontrado, reintentando en 2s...")
                    self.bluetoothConnected = False
                    time.sleep(2)
                    continue
                print (f"Conectado a:{self.gamepad.name}({self.gamepad.path})")
                self.bluetoothConnected = True
                if self._funcion:
                    self.command = -2
                    self._funcion(self.command)

            try:
                self.bluetoothConnected = True
                for event in self.gamepad.read_loop():
                #filters by event type
                    #print(event.code)
                    #Evento al pulsar las teclas del joystick
                    self.flag = 1
                    if (event.type == ecodes.EV_KEY and event.value == 1):
                        #print(event)
                        #ser.write(b"hola mundo")
                        #print(int(event.code))
                        if event.code == 304:
                            #code = 1;
                            #ser.write(str("s").encode())
                            #ser.write(bytes([code]))
                            #ser.write(bytes([27]))
                            self.command = 27
                            
                        elif event.code == 305:
                            #code = 1;
                            #ser.write(str("s").encode())
                            #ser.write(bytes([code]))
                            #ser.write(bytes([27]))
                            self.command = 27
                            
                        elif (event.code == 308):
                            #code = 1;
                            #ser.write(str("s").encode())
                            #ser.write(bytes([code]))
                            #ser.write(bytes([27]))
                            self.command = 27
                            
                        elif event.code == 307:
                            #code = 1;
                            #ser.write(str("s").encode())
                            #ser.write(bytes([code]))
                            #ser.write(bytes([27]))
                            self.command = 27
                            
                        elif event.code == 311:
                            #code = 1;
                            ##ser.write(str("u").encode())
                            #ser.write(bytes([18]))
                            self.command = 18
                            
                        elif event.code == 310:
                            #code = 1;
                            #ser.write(str("d").encode())
                            #ser.write(bytes([code]))
                            #ser.write(bytes([23]))
                            self.command = 23
                        #print(self.command)
                        if self._funcion:
                            self._funcion(self.command) 
                        
                    #Evento al liberar las teclas del JOystick
                    if (event.type == ecodes.EV_KEY and event.value == 0):
                        #print(event)
                        #ser.write(b"hola mundo")
                        #print(int(event.code))
                        if event.code == 304:
                            #code = 0;
                            #ser.write(str("S").encode())
                            #ser.write(bytes([code]))
                            #ser.write(bytes([29]))
                            self.command = 29
                            
                        elif event.code == 305:
                            #code = 0;
                            #ser.write(str("S").encode())
                            #ser.write(bytes([code]))
                            #ser.write(bytes([29]))
                            self.command = 29
                            
                        elif (event.code == 308):
                            #code = 0;
                            #ser.write(str("S").encode())
                            #ser.write(bytes([code]))
                            #ser.write(bytes([29]))
                            self.command = 29
                            
                        elif event.code == 307:
                            #code = 0;
                            #ser.write(str("S").encode())
                            #ser.write(bytes([code]))
                            #ser.write(bytes([29]))
                            self.command = 29
                            
                        elif event.code == 311:
                            #code = 0;
                            #ser.write(str("U").encode())
                            #ser.write(bytes([20]))
                            self.command = 20
                            
                        elif event.code == 310:
                            #code = 0;
                            #ser.write(str("D").encode())
                            #ser.write(bytes([24]))
                            self.command = 24
                        #print(self.command)
                        
                    
                        
                        #print(type(event.code))
                        #ser.write(b'Write counter: %d \n'%(counter))
                        #ser.write(event.type)
                        #print("printed")
                        #time.sleep(1)
                        #counter += 1
                        
                        if self._funcion:
                            self._funcion(self.command)

                    #Eventos en el movimiento del Joystick
                    elif event.type == ecodes.EV_ABS:
                        absevent = categorize(event)
                        #print (ecodes.bytype[absevent.event.type][absevent.event.code], absevent.event.value)
                        if ecodes.bytype[absevent.event.type][absevent.event.code] == "ABS_X":
                        #if absevent.event.code == 0:
                            #print("eje x")
                            #ser.write(str("x").encode())
                            #print("Valor eje X", absevent.event.value)
                            #ser.write(bytes([absevent.event.value]))
                            self.Xcode = absevent.event.value
                            
                            #joyState()
                            
                        #elif absevent.event.code == 1:
                        if ecodes.bytype[absevent.event.type][absevent.event.code] == "ABS_Y":
                            #print("eje y")
                            #ser.write(str("y").encode())
                            #print("Valor eje Y", absevent.event.value)
                            #ser.write(bytes([absevent.event.value]))
                            self.Ycode = absevent.event.value
                        if ecodes.bytype[absevent.event.type][absevent.event.code] == "ABS_Z":
                            #X mando derecho
                            pass
                        if ecodes.bytype[absevent.event.type][absevent.event.code] == "ABS_RZ":
                            #Y mando derecho
                            pass
                        if ecodes.bytype[absevent.event.type][absevent.event.code] == "ABS_BRAKE":
                            #L2
                            pass
                        if ecodes.bytype[absevent.event.type][absevent.event.code] == "ABS_GAS":
                            #R2
                            pass
                        if ecodes.bytype[absevent.event.type][absevent.event.code] == "ABS_HAT0X":
                            #Cruceta ejeX
                            self.Xcruccode = absevent.event.value
                            
                        if ecodes.bytype[absevent.event.type][absevent.event.code] == "ABS_HAT0Y":
                            #Cruceta ejeY
                            self.Ycruccode = absevent.event.value
                            
                        #self.joyState()# descomentar para usar el joystick analógico
                        self.CrucetaState() # descomentar para usar la cruceta digital
                        """ print(self.Xcode, self.Ycode)
                        print(self.Xcode)
                        print(self.Ycode) """
            except OSError:
                
                self.bluetoothConnected = False
                #print("Se ha perdido la Conexion, rompiendo hilo")
                self.gamepad = None
                if self._funcion:
                    
                    self.command = -1
                    self._funcion(self.command)
                time.sleep(2)

    def joyState( self ):
        #Xaxys_ant = Xmem
        #Yaxys_ant = Ymem
        x = self.Xcode
        y = self.Ycode
        print(x,y)
        """ self.XY = self.Xcode * 1000 + self.Ycode
        extractX = self.XY // 1000
        extractY = self.XY % 1000
        print(self.XY)
        print(self.XY) """
        packet = (x << 8) | y
        print(packet)
        self.command = packet
        if self._funcion:
            self._funcion(self.command)
        """ x = (packet >> 8) & 0xff
        y = packet & 0xff """
        print(x, y)

        #print (str(self.Xcode)+","+str(self.Ycode))
    def CrucetaState( self ):
        x = self.Xcruccode
        y = self.Ycruccode
        print(x,y)
        #print ( Xaxys_ant, Yaxys_ant, x, y)
        if ( x == 0 and y == -1):
            #ser.write(str("UP").encode())
            #ser.write(bytes([3]))
            self.command = 3
            
        elif ( x == -1 and y == 0):
            #ser.write(str("LEFT").encode())
            #ser.write(bytes([6]))
            self.command = 6
        elif ( x == 0 and y == 1):
            #ser.write(str("DOWN").encode())
            #ser.write(bytes([5]))
            self.command = 5
        elif ( x ==1 and y == 0):
            #ser.write(str("RIGHT").encode())
            #ser.write(bytes([9]))
            self.command = 9
        elif ( x == -1 and y == -1):
            #ser.write(str("LeftUp").encode())
            #ser.write(bytes([12]))
            self.command = 12
        elif ( x == -1 and y == 1 ):
            #ser.write(str("LeftDown").encode())
            #ser.write(bytes([17]))
            self.command = 17
        elif ( x == 1 and y == 1 ):
            #ser.write(str("RightDown").encode())
            #ser.write(bytes([15]))
            self.command = 15
        elif ( x == 1 and y == -1 ):
            #ser.write(str("RightUp").encode())
            #ser.write(bytes([10]))
            self.command = 10
        elif ( x == 0 and y == 0 ):
            #ser.write(str("CENTER").encode())
            #ser.write(bytes([0]))
            self.command = 0
        #print(self.command)
        if self._funcion:
            self._funcion(self.command)
            
        #return          
        
        
            
    #evdev takes care of polling the controller in a loop