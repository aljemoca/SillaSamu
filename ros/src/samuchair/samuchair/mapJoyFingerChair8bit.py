from evdev import InputDevice, ecodes, list_devices
import threading
import time


class ComJoyBluetooth:

    def __init__(self):

        print("[INIT] 8BitDo analog joystick init")

        self.gamepad = None
        self.stop_event = threading.Event()

        # analog sticks raw
        self.LX = 32768
        self.LY = 32768

        self.CENTER = 32768
        self.DEADZONE = 8000

        # output motor style (igual que tu sistema actual)
        self.motor_x = 160
        self.motor_y = 160

        self._funcion = None

        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()

    # -----------------------------
    # FIND DEVICE
    # -----------------------------
    def find_device(self):

        print("[SCAN] buscando 8BitDo...")

        for path in list_devices():
            dev = InputDevice(path)
            name = dev.name.lower()

            print(f"[SCAN] {dev.path} -> {dev.name}")

            if "8bitdo" in name or "sf30" in name:
                print(f"[OK] conectado: {dev.name}")
                return InputDevice(path)

        print("[FAIL] no encontrado")
        return None

    # -----------------------------
    # LOOP
    # -----------------------------
    def run(self):

        print("[RUN] thread joystick iniciado")

        while not self.stop_event.is_set():

            if not self.gamepad:
                self.gamepad = self.find_device()

                if not self.gamepad:
                    time.sleep(2)
                    continue

                print("[CONN] joystick conectado")

            try:

                for event in self.gamepad.read_loop():

                    # DEBUG RAW
                    print(f"[RAW] type={event.type} code={event.code} value={event.value}")

                    if event.type == ecodes.EV_ABS:

                        # STICK IZQUIERDO (principal)
                        if event.code == ecodes.ABS_X:
                            self.LX = event.value
                            print(f"[LX] {self.LX}")

                        elif event.code == ecodes.ABS_Y:
                            self.LY = event.value
                            print(f"[LY] {self.LY}")

                        self.compute_motion()

            except OSError:
                print("[ERROR] desconectado")
                self.gamepad = None
                time.sleep(2)

    # -----------------------------
    # ANALOG -> MOTOR
    # -----------------------------
    """ def compute_motion(self):

        # normalización -1..1
        lx = (self.LX - self.CENTER) / self.CENTER
        ly = (self.LY - self.CENTER) / self.CENTER

        # DEBUG NORMALIZADO
        print(f"[NORM] LX={lx:.2f} LY={ly:.2f}")

        # deadzone
        if abs(lx) < 0.15:
            lx = 0
        if abs(ly) < 0.15:
            ly = 0

        # -----------------------------
        # MAPEO DIRECTO A MOTORES
        # -----------------------------
        # tu sistema usa:
        # 160 = stop
        # 255 = forward
        # 0   = backward

        forward = -ly  # invertido típico joystick

        base = 160

        # velocidad avance/retroceso
        motor_y = base + (forward * 95)

        # giro diferencial (izquierda/derecha)
        motor_x = base + (lx * 95)

        # clamp
        motor_x = max(0, min(255, int(motor_x)))
        motor_y = max(0, min(255, int(motor_y)))

        self.motor_x = motor_x
        self.motor_y = motor_y

        print(f"[MOTOR] X={self.motor_x} Y={self.motor_y}")

        # callback hacia ROS2
        if self._funcion:
            self._funcion((self.motor_x, self.motor_y)) """

    def compute_motion(self):

        # -----------------------------
        # NORMALIZACIÓN
        # -----------------------------
        lx = (self.LX - self.CENTER) / self.CENTER
        ly = (self.LY - self.CENTER) / self.CENTER

        print(f"[NORM] LX={lx:.2f} LY={ly:.2f}")

        # DEADZONE
        if abs(lx) < 0.15:
            lx = 0
        if abs(ly) < 0.15:
            ly = 0

        # -----------------------------
        # CONTROL PRINCIPAL
        # -----------------------------
        # velocidad (adelante/atrás)
        speed = -ly  # invertir eje Y

        # giro
        turn = lx

        # -----------------------------
        # ESCALADO A MOTOR (0–255)
        # centro = 160
        # -----------------------------
        BASE = 160
        SCALE = 95

        # mezcla diferencial REAL
        left_motor  = BASE + (speed * SCALE) - (turn * SCALE)
        right_motor = BASE + (speed * SCALE) + (turn * SCALE)

        # clamp
        left_motor = max(0, min(255, int(left_motor)))
        right_motor = max(0, min(255, int(right_motor)))

        self.motor_left = left_motor
        self.motor_right = right_motor

        print(f"[MOTOR] L={self.motor_left} R={self.motor_right}")

        if self._funcion:
            self._funcion((self.motor_left, self.motor_right))

    # -----------------------------
    def set_callback(self, func):
        self._funcion = func

    def stop(self):
        print("[STOP]")
        self.stop_event.set()
        self.thread.join()