from evdev import InputDevice, ecodes, list_devices
import threading
import time


class ComJoyBluetooth:

    def __init__(self):

        print("[INIT] 8BitDo analog joystick init")
        self.bluetoothConnected = False
        self.gamepad = None
        self.stop_event = threading.Event()

        # -------- CONFIG REAL (TU JOYSTICK) --------
        self.AXIS_X = 0  # ABS_X
        self.AXIS_Y = 1  # ABS_Y

        self.MIN = 0
        self.MAX = 255
        self.CENTER = 128   
        self.DEADZONE = 8  

 # -------- ESTADO --------
        self.raw_x = self.CENTER
        self.raw_y = self.CENTER

        self._funcion = None

        # -------- SUAVIZADO --------
        self.current_left = 0.0
        self.current_right = 0.0
        self.RAMP_STEP = 0.04  # un poco más suave

        # -------- CALLBACK --------
        self._callback = None

        # -------- HILO --------
        self.thread = threading.Thread(target=self.run)
        self.thread.start()
    # -----------------------------
    # BUSCAR DISPOSITIVO
    # -----------------------------
    def find_device(self):

        print("[SCAN] buscando 8BitDo...")

        for path in list_devices():
            dev = InputDevice(path)
            name = dev.name.lower()

            print(f"[SCAN] {dev.path} -> {dev.name}")

            if "8bitdo" in name or "sf30" in name:
                print(f"[OK] conectado: {dev.name}")
                self.bluetoothConnected = True
                return InputDevice(path)

        print("[FAIL] no encontrado")
        return None
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
    # -----------------------------
    # LOOP PRINCIPAL
    # -----------------------------
    def run(self):

        print("[RUN] thread joystick iniciado")

        while not self.stop_event.is_set():

            if not self.gamepad:
                self.gamepad = self.find_device()
               
                if not self.gamepad:
                    print("[WARN] Buscando joystick...")
                    self.bluetoothConnected = False
                    time.sleep(2)
                    continue
                self.bluetoothConnected = True
                if self._funcion:
                    self.command = -2
                    self._funcion(self.command)
                print("[CONN] joystick conectado")

            try:
                for event in self.gamepad.read_loop():

                    if event.type == ecodes.EV_ABS:

                        if event.code == self.AXIS_X:
                            self.raw_x = event.value

                        elif event.code == self.AXIS_Y:
                            self.raw_y = event.value

                        self.process()

            except OSError:
                print("[ERROR] Joystick desconectado")
                self.bluetoothConnected = False
                self.gamepad = None

                if self._callback:
                    self._callback(160, 160)

                time.sleep(2)

    # -------- NORMALIZACIÓN --------
    def normalize(self, value):
        if abs(value - self.CENTER) < self.DEADZONE:
            return 0.0

        if value > self.CENTER:
            return (value - self.CENTER) / (self.MAX - self.CENTER)
        else:
            return (value - self.CENTER) / (self.CENTER - self.MIN)
    # -----------------------------
    
     # -------- MEZCLA DIFERENCIAL --------
    def compute_motors(self):
        # 🔥 IMPORTANTE: invertimos Y (arriba = adelante)
        throttle = -(self.normalize(self.raw_y))
        steering = self.normalize(self.raw_x)

        left = throttle + steering
        right = throttle - steering

        left = max(-1, min(1, left))
        right = max(-1, min(1, right))

        return left, right

    # -------- SUAVIZADO --------
    def ramp(self, current, target):
        if current < target:
            current += self.RAMP_STEP
            if current > target:
                current = target
        elif current > target:
            current -= self.RAMP_STEP
            if current < target:
                current = target
        return current

    # -------- ESCALA FINAL --------
    def to_arduino(self, value):
        # Mantiene compatibilidad con tu sistema (centro ~160)
        return int(160 + value * 100)

    # -------- PROCESAMIENTO --------
    def process(self):
        target_l, target_r = self.compute_motors()

        # suavizado
        self.current_left = self.ramp(self.current_left, target_l)
        self.current_right = self.ramp(self.current_right, target_r)

        x = self.to_arduino(self.current_left)
        y = self.to_arduino(self.current_right)

        # DEBUG limpio
        print(f"[JOY] X:{self.raw_x} Y:{self.raw_y} -> L:{x} R:{y}")

        # salida directa
        packed = x * 1000 + y

        print(f"[CLASS] Enviando packed: {packed} ({x},{y})")  # DEBUG

        if self._callback:
            self._callback(packed)

    # -------- CALLBACK --------
    def set_callback(self, func):
        self._callback = func

    def stop(self):
        self.stop_event.set()
        self.thread.join()