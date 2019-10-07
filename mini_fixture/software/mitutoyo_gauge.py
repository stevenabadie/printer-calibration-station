import threading

class readDialGauge():
    def __init__(self):
        self.reading = ""

    # Need to add safety for when gauge is not on or disconnected but switch is connected.

    def read_gauge(self):
        self.reading = input()

    def hit_switch(self, serial, command):
        serial.write((command).encode("utf-8"))

    def get_dial_reading(self, serial):
        t = threading.Timer(0.3, self.hit_switch, args=(serial, 'A\r\n')).start()
        self.read_gauge()
        return self.reading
