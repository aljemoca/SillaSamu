import serial
from time import sleep
import time



class ComJoystickManual:
    
    def __init__(self):
        self.puerto='/dev/Joystick'
        #self.puerto='/dev/ttyUSB0'
        #self.buscaPuerto()
        self.x=0
        self.y=0
        self.local = True
        self.ser = None
        self.connected = False
        self.sec_est_puerto = False
        self.last_attempt = 0
        self.reconnect_interval = 5.0   # segundos
        #self.actualizaEstado()
        return
    
    def __del__(self):
        if  self.connected:
            self.ser.close()

    def safe_write(self, data):
        # if not self.ensure_connection():
        #    return False
#        print(f'Safe_write_Connected:{self.connected}')
        if not self.connected:
            return False
        try:
            self.ser.write(data)
            return True
        except:
            self.connected = False
            return False

    def safe_read(self, size=1):
#         if not self.ensure_connection():
#              return ''
# #        print(f'Safe_read_Connected:{self.connected}')
        if not self.connected:
            return ''
        try:
            return self.ser.read(size).decode()
        except:
            self.connected = False
            return ''



    def ensure_connection(self):
        if self.connected:
            return True
        
        now = time.time()
        if now - self.last_attempt < self.reconnect_interval:
            return False
        
        self.last_attempt = now
        return self.establecePuerto(self.puerto)


    def	conectado(self):
        return self.connected
    
    def esLocal(self):
        self.actualizaEstado()
        return self.local

    def esRemoto(self):
        self.actualizaEstado()
        return not self.local
    
    def esJoystick(self):
        #print(f'Secuencia Puerto:{self.sec_est_puerto}'  )
        if self.sec_est_puerto:
            self.ser.write('Ix'.encode())
        else:
            self.safe_write('Ix'.encode())
        sleep(0.1)        
        return self.esperaRespuesta('A')
    
    def esperaRespuesta(self,respuesta):
        buffer = [0,0,0,0,0]
        ok = False
        cont = 0
        ind=0
        car = 0
        res=''
        while car!='x' and cont<=4:
            if self.sec_est_puerto is True:
                car = self.ser.read().decode()
            else:
                car = self.safe_read()
            buffer[ind] = car
            #print(buffer)
            if buffer[ind].upper() >='A' and buffer[ind].upper()<='Z' :
                ind+=1
            cont+=1
        #print(ind)
        if	ind>0:
            res = ''.join(str(e) for e in buffer[:ind-1])
        #print(res)
        if res==respuesta:
            ok=True
        
        return ok
    
    
    def	esOk(self):
        return self.esperaRespuesta('Ok')
    

 
            
    def consultaPuerto(self):
        return self.puerto
    
    def establecePuerto(self,puerto):
        cont=0
        ok=False
        self.sec_est_puerto = True
        print(puerto)
        try:
            self.ser=serial.Serial(port=puerto, baudrate=115200,timeout=0.5)
            
            sleep(2.0)
            while cont<3:
                if self.esJoystick():
                    print('Conectado al puerto=' +puerto)
                    self.puerto=puerto
                    self.connected = True
                    ok=True
                    self.sec_est_puerto=False
                    return ok
                cont+=1
            self.ser.close()
        except:
                #print("No hay puerto"+portname)
            print('No fue posible la conexión al puerto '+ puerto)
            self.connected=False
            #self.puerto=None
        #print(self.sec_est_puerto)
        return ok
    
    def controlRemoto(self):
        comando = 'C1x'.encode()
        #self.ser.write(comando)
        self.safe_write(comando)
        sleep(0.1)
        if self.esOk():
            self.local=False
        if not self.local:
            if not self.escribeMandos(160,160):  #Poner valores por defecto para que la silla esté parada
                self.local = True
        return not self.local
        
    def controlLocal(self):
        
        comando = 'C0x'.encode()
        #self.ser.write(comando)
        self.safe_write(comando)
        sleep(0.1)
        ok = self.esOk()
        self.local = ok
        return self.local

    def escribeMandos(self,x,y):
        self.x = x
        self.y = y
        comando = 'J'+str(self.x)+','+str(self.y)+('x')
        #print(comando)
        #self.ser.write(comando.encode())
        self.safe_write(comando.encode())
        sleep(0.1)
        return self.esOk()
    
    def consultaXY(self):
        res  = True
        if self.esLocal():
            res =self.actualizaXY();
        return res, self.x,self.y
    
    
    def actualizaEstado(self):
        comando = 'Sx'.encode();
        #self.ser.write(comando);
        self.safe_write(comando);
        sleep(0.1)
        buffer = list([0]*5)
        ok = False
        ind=0
        car=0
        res=''
        while car!='x' and ind<=4:
            #buffer[ind] = self.ser.read().decode()
            buffer[ind] = self.safe_read()
            car=buffer[ind]
            ind+=1
        if	ind>0:
            res = ''.join(str(e) for e in buffer[:ind-1])
            if self.connected:
                ok = True
        print(buffer)
        if len(res)>1 and self.connected:
            if res[1] =='0':
                self.local = True
            else:

                self.local=False
        print('Local:'+str(self.local))
        return ok   
    
    def actualizaXY(self):
        comando='Rx'.encode();
        #self.ser.write(comando)
        self.safe_write(comando)
        sleep(0.1)
        buffer = list([0]*10)
        ok = False
        ind=0
        car =0
        res=''
        while car!='x' and ind<10:
            #buffer[ind] = self.ser.read().decode()
            buffer[ind] = self.safe_read()
            car = buffer[ind]
            ind+=1
        if	ind>0:
            res = ''.join(str(e) for e in buffer[:ind-1])
            #print(res)
        if len(res)>1 and self.connected:
            res[1:].split(',')
            cadena= res[1:].split(',')
            self.x = int(cadena[0])
            self.y = int(cadena[1])
            ok=True
        return ok
# class ComJoystickManual:
    
#     def __init__(self):
#         self.puerto=''
#         #self.buscaPuerto()
#         self.x=0
#         self.y=0
#         self.local = True
#         self.conexion = False
#         #self.actualizaEstado()
#         return
    
#     def __del__(self):
#         self.ser.close()

#     def	conectado(self):
#         return self.conexion
    
#     def esLocal(self):
#         ok=self.actualizaEstado()
#         return self.local

#     def esRemoto(self):
#         self.actualizaEstado()
#         return not self.local
    
#     def esJoystick(self):
#         comando = 'Ix'.encode();
#         self.ser.write(comando);
#         return self.esperaRespuesta('A')
    
#     def esperaRespuesta(self,respuesta):
#         buffer = [0,0,0,0,0]
#         ok = False
#         cont = 0
#         ind=0
#         car = 0
#         res=''
#         while car!='x' and cont<=4:
#             buffer[ind] = self.ser.read().decode()
#             car=buffer[ind]
#             #print(buffer)
#             if buffer[ind].upper() >='A' and buffer[ind].upper()<='Z' :
#                 ind+=1
#             cont+=1
#         #print(ind)
#         if	ind>0:
#             res = ''.join(str(e) for e in buffer[:ind-1])
#             if buffer[ind-1]=='x':
#                 self.conexion=True
#             else:
#                 self.conexion=False
#         #print(res)
#         if res==respuesta:
#             ok=True
        
#         return ok
    
    
#     def	esOk(self):
#         return self.esperaRespuesta('Ok')
    
#     def	buscaPuerto(self):
#         raiz='/dev/ttyUSB'
#         mensaje="Buscando puerto para el control del motor"
#         sleep(2.0)
#         print(mensaje)
#         ok=False
#         for p in range(4):
#             portname=raiz+str(p)
#             ser=[]
#             if(self.establecePuerto(portname)):
#                 ok=True;
#                 return ok
#         return ok
 
            
#     def consultaPuerto(self):
#         return self.puerto
    
#     def establecePuerto(self,puerto):
#         ok=False
#         cont=0
#         print(puerto)
#         try:
#             self.ser=serial.Serial(port=puerto, baudrate=115200,timeout=0.5)
#             #print(self.ser)
#             sleep(2.0)
#             while cont<3:
#                 self.ser.write('Ix'.encode())
#                 sleep(0.1)
#                 if self.esJoystick():
#                     print('Conectado al puerto=' +puerto)
#                     self.puerto=puerto
#                     ok=True
#                     self.conexion=True
#                     break
#                 cont+=1
#         except:
#                 #print("No hay puerto"+portname)
#             print('No fue posible la conexión al puerto '+ puerto)
#             self.conexion=False

#         return ok
    
#     def controlRemoto(self):
#         comando = 'C1x'.encode()
#         self.ser.write(comando)
#         sleep(0.1)
#         if self.esOk():
#             self.local=False
#             self.conexion=True
#         if not self.local:
#             if not self.escribeMandos(128,128):  #Poner valores por defecto para que la silla esté parada
#                 self.local = True
#         return not self.local
        
#     def controlLocal(self):
        
#         comando = 'C0x'.encode()
#         self.ser.write(comando)
#         sleep(0.1)
#         ok = self.esOk()
#         self.local = ok
#         return self.local

#     def escribeMandos(self,x,y):
#         self.x = x
#         self.y = y
#         comando = 'J'+str(self.x)+','+str(self.y)+('x')
#         #print(comando)
#         self.ser.write(comando.encode())
#         sleep(0.1)
#         return self.esOk()
    
#     def consultaXY(self):
#         res  = True
#         if self.local:
#             res =self.actualizaXY();
#         return res, self.x,self.y
    
    
#     def actualizaEstado(self):
#         comando = 'Sx'.encode();
#         self.ser.write(comando);
#         sleep(0.1)
#         buffer = list([0]*5)
#         ok = False
#         ind=0
#         car=0
#         res=''
#         while car!='x' and ind<=4:
#             buffer[ind] = self.ser.read().decode()
#             car=buffer[ind]
#             ind+=1
#         if	ind>0:
#             res = ''.join(str(e) for e in buffer[:ind-1])
#             if buffer[ind-1]=='x':
#                 ok = True
#                 self.conexion=True
#             else:
#                 self.conexion=False
#         print(buffer)
#         if res[1] =='0':
#             self.local = True
#         else:
#             self.local=False
#         #print('Local:'+str(self.local))
#         return ok   
    
#     def actualizaXY(self):
#         comando='Rx'.encode();
#         self.ser.write(comando)
#         sleep(0.1)
#         buffer = list([0]*15)
#         ok = False
#         ind=0
#         car =0
#         res=''
#         while car!='x' and ind<11:
#             car = self.ser.read().decode()
#             buffer[ind] = car
#             ind+=1
#         if	ind>0:
#             res = ''.join(str(e) for e in buffer[:ind-1])
#             if buffer[ind-1]=='x':
#                 ok=True
#                 self.conexion=True
#             else:
#                 self.conexion=False
#             print(res)
#         res[1:].split(',')
#         cadena= res[1:].split(',')
#         self.x = int(cadena[0])
#         self.y = int(cadena[1])
#         return ok
