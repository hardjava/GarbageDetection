import serial

class ArduinoController:
    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate
        self.timeout =.1
        self.arduino = None

    def connect(self):
        self.arduino = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=self.timeout)

    def read_arduino(self):
        data = self.arduino.readline()[:-2]
        if data:
            return data.decode('utf-8')
    
    def write_arduino(self, data):
        self.arduino.write(data)
        print(f"write: '{data}'")

    def write_lcd(self, data):
        if data == 'glass':
            self.arduino.write(b'2')
        elif data == 'metal':
            self.arduino.write(b'3')
        elif data == 'paper':
            self.arduino.write(b'4')
        elif data == 'plastic':
            self.arduino.write(b'5')
    
    def write_rotation(self, data):
        if data == 'plastic':
            self.arduino.write(b'0')
        elif data == 'metal':
            self.arduino.write(b'1')
        elif data == 'paper':
            self.arduino.write(b'2')

    def disconnect(self):
        self.arduino.close()