import threading
from time import sleep
from nextech_gauge import nextechReading

class dragTest():
    def __init__(self):
        self.nextech = nextechReading()
        self.printer_level_x = 'gcodes/machine_X_level.gcode'
        self.printer_prep_x = 'gcodes/machine_X_drag.gcode'
        self.printer_prep_y = 'gcodes/machine_Y_drag.gcode'
        self.printer_prep_z = 'gcodes/machine_Z_drag.gcode'
        self.actuator_drag_x = 'gcodes/fixture_X_drag_calibration.gcode'
        self.actuator_drag_y = 'gcodes/fixture_Y_drag_calibration.gcode'
        self.actuator_drag_z = 'gcodes/fixture_Z_drag_calibration.gcode'

    def run_gcode(self, devices, device, gcode):
        with open(gcode, 'r') as gcode:
            gcode_lines = gcode.read().splitlines()
        for line in gcode_lines:
            devices.ports[device].write(('\r\n' + line + '\r\n').encode('utf-8'))

    def printer_x_level(self, devices):
        self.run_gcode(devices, 'printer', self.printer_level_x)

    def printer_x_prep(self, devices):
        self.run_gcode(devices, 'printer', self.printer_prep_x)

    def printer_y_prep(self, devices):
        self.run_gcode(devices, 'printer', self.printer_prep_y)

    def printer_z_prep(self, devices):
        self.run_gcode(devices, 'printer', self.printer_prep_z)

    def x_drag_actuate(self, devices):
        self.run_gcode(devices, 'actuator', self.actuator_drag_x)

    def y_drag_actuate(self, devices):
        self.run_gcode(devices, 'actuator', self.actuator_drag_y)

    def z_drag_actuate(self, devices):
        self.run_gcode(devices, 'actuator', self.actuator_drag_z)

    def run_drag_test(self, actuate_delay, command, devices, drag_function, gauge, prep_delay, prep_function, readings):
        zero_gauge = self.nextech.zero_gauge(devices, gauge)
        prep_function(devices)
        sleep(prep_delay)
        reading = []
        t = threading.Timer(actuate_delay, drag_function, args=(devices,)).start()
        reading_count = readings
        while reading_count != 0:
            reading.append(self.nextech.get_clean_force_reading(devices, gauge, command))
            reading_count -= 1
            sleep(0.5)
        return reading

    def x_drag_test(self, devices, command):
        reading = self.run_drag_test(0, command, devices, self.x_drag_actuate, 'dfs_xz', 12.0, self.printer_x_prep, 80)
        return reading

    def y_drag_test(self, devices, command):
        reading = self.run_drag_test(8, command, devices, self.y_drag_actuate, 'dfs_y', 5.0, self.printer_y_prep, 100)
        return reading

    def z_drag_test(self, devices, command):
        reading = self.run_drag_test(4, command, devices, self.z_drag_actuate, 'dfs_xz', 15.0, self.printer_z_prep, 80)
        return reading


