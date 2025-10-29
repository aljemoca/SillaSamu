import serial
from time import sleep


class ComJoystickManual:
    
    def __init__(self):
        self.puerto=''
        #self.buscaPuerto()
        self.x=0
        self.y=0
        self.local = True
        #self.actualizaEstado()
        return
    
    def __del__(self):
        self.ser.close()

    def	conectado(self):
        ok=True
        if self.puerto=='':
            ok=False
        return ok
    
    def esLocal(self):
        self.actualizaEstado()
        return self.local

    def esRemoto(self):
        self.actualizaEstado()
        return not self.local
    
    def esJoystick(self):
        return self.esperaRespuesta('A')
    
    def esperaRespuesta(self,respuesta):
        buffer = [0,0,0,0,0]
        ok = False
        cont = 0
        ind=0
        car = 0
        res=''
        while car!='x' and cont<=4:
            buffer[ind] = self.ser.read().decode()
            car=buffer[ind]
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
            self.ser=serial.Serial(port=puerto, baudrate=115200,timeout=0.5)
            #print(self.ser)
            sleep(2.0)
            while cont<3:
                self.ser.write('Ix'.encode())
                sleep(0.1)
                if self.esJoystick():
                    print('Conectado al puerto=' +puerto)
                    self.puerto=puerto
                    ok=True
                    break
                cont+=1
        except:
                #print("No hay puerto"+portname)
            print('No fue posible la conexión al puerto '+ puerto)


        return ok
    
    def controlRemoto(self):
        comando = 'C1x'.encode()
        self.ser.write(comando)
        sleep(0.1)
        if self.esOk():
            self.local=False
        if not self.local:
            if not self.escribeMandos(128,128):  #Poner valores por defecto para que la silla esté parada
                self.local = True
        return not self.local
        
    def controlLocal(self):
        
        comando = 'C0x'.encode()
        self.ser.write(comando)
        sleep(0.1)
        ok = self.esOk()
        self.local = ok
        return self.local

    def escribeMandos(self,x,y):
        self.x = x
        self.y = y
        comando = 'J'+str(self.x)+','+str(self.y)+('x')
        #print(comando)
        self.ser.write(comando.encode())
        sleep(0.1)
        return self.esOk()
    
    def consultaXY(self):
        res  = True
        if self.local:
            res =self.actualizaXY();
        return res, self.x,self.y
    
    
    def actualizaEstado(self):
        comando = 'Sx'.encode();
        self.ser.write(comando);
        sleep(0.1)
        buffer = list([0]*5)
        ok = False
        ind=0
        car=0
        res=''
        while car!='x' and ind<=4:
            buffer[ind] = self.ser.read().decode()
            car=buffer[ind]
            ind+=1
        if	ind>0:
            res = ''.join(str(e) for e in buffer[:ind-1])
            ok = True
        print(buffer)
        if res[1] =='0':
            self.local = True
        else:
            self.local=False
        print('Local:'+str(self.local))
        return ok   
    
    def actualizaXY(self):
        comando='Rx'.encode();
        self.ser.write(comando)
        sleep(0.1)
        buffer = list([0]*10)
        ok = False
        ind=0
        car =0
        res=''
        while car!='x' and ind<=10:
            buffer[ind] = self.ser.read().decode()
            ind+=1
        if	ind>0:
            res = ''.join(str(e) for e in buffer[:ind-1])
            ok=True
            #print(res)
        res[1:].split(',')
        cadena= res[1:].split(',')
        self.x = int(cadena[0])
        self.y = int(cadena[1])
        return ok
