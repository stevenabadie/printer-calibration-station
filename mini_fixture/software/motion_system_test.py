import connect_hardware
import drag_test
import accuracy_test

class motionSystemTest():
    def __init__(self):
        self.connected_hardware = connect_hardware.connectHardware()
        self.dt = drag_test.dragTest()
        self.at = accuracy_test.accuracyTest()
