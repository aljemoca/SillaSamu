import gpiod
import os
import time



class Puerto:
    def __init__(self):
        
        self.pin = None
        self.CHIP = "gpiochip4"
        self.LINE = None

        
       
      

    def pinModeIn(self,pin):
         
        try:
            self.chip = gpiod.Chip(self.CHIP)
            self.line= self.chip.get_line( pin )
            self.line.request(consumer="shutdown-button", 
            type=gpiod.LINE_REQ_DIR_IN, 
            flags=gpiod.LINE_REQ_FLAG_BIAS_PULL_DOWN)
            
            
      #  self.temp_value=0
      #  self.counter=0
      #  self.hilo = threading.Thread(target=self._hilo_callback)
      #  self.hilo.start()

        except FileNotFoundError:
            print(f"ERROR: No se encontró el chip GPIO '{self.CHIP}' en '/dev/'.")
            print("Asegúrate de que el nombre del chip sea correcto para tu Pi 5 y que los controladores estén cargados.")
        except PermissionError:
            print(f"ERROR: Permiso denegado para acceder al chip GPIO '{self.CHIP}'.")
            print(f"Asegúrate de que tu usuario ('{os.getlogin()}') esté en el grupo 'dialout' y que hayas REINICIADO la Pi.")
        except gpiod.InvalidLineError:
            print(f"ERROR: El pin {self.LINE} no es válido en el chip {self.CHIP}.")
            print("Verifica el número del pin BCM para tu Raspberry Pi 5.")
    # Usa el gpiod.Error general para cualquier otro problema específico de gpiod
        except gpiod.Error as e: 
            print(f"ERROR: Se produjo un error específico de gpiod: {e}")
        except Exception as e:
            print(f"ERROR: Se produjo un error inesperado: {e}")
        except KeyboardInterrupt:
            print("Script cancelado por el usuario.")
            
    def pinModeOut(self,pin):
         
        try:
            self.chip = gpiod.Chip(self.CHIP)
            self.line= self.chip.get_line( pin )
            self.line.request(consumer="shutdown-button", 
            type=gpiod.LINE_REQ_DIR_OUT, 
            default_vals=[0])
            
            
      #  self.temp_value=0
      #  self.counter=0
      #  self.hilo = threading.Thread(target=self._hilo_callback)
      #  self.hilo.start()

        except FileNotFoundError:
            print(f"ERROR: No se encontró el chip GPIO '{self.CHIP}' en '/dev/'.")
            print("Asegúrate de que el nombre del chip sea correcto para tu Pi 5 y que los controladores estén cargados.")
        except PermissionError:
            print(f"ERROR: Permiso denegado para acceder al chip GPIO '{self.CHIP}'.")
            print(f"Asegúrate de que tu usuario ('{os.getlogin()}') esté en el grupo 'dialout' y que hayas REINICIADO la Pi.")
        except gpiod.InvalidLineError:
            print(f"ERROR: El pin {self.LINE} no es válido en el chip {self.CHIP}.")
            print("Verifica el número del pin BCM para tu Raspberry Pi 5.")
    # Usa el gpiod.Error general para cualquier otro problema específico de gpiod
        except gpiod.Error as e: 
            print(f"ERROR: Se produjo un error específico de gpiod: {e}")
        except Exception as e:
            print(f"ERROR: Se produjo un error inesperado: {e}")
        except KeyboardInterrupt:
            print("Script cancelado por el usuario.")
            
                 
    def digitalWrite(self, value):
        self.line.set_value(value)
        
    def digitalRead(self):
        val = self.line.get_value()
        return (val)
    #
    #def _hilo_callback(self):
    #    self.counter=self.counter+1
    #    print('.')
    #    if self.counter==5:
    #        self.counter=0
        #time.sleep(0.5)  #Cambiar a 0.1
