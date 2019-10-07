import threading
from time import sleep
from mitutoyo_gauge import readDialGauge


class accuracyTest():
    def __init__(self):
        self.mt_gauge = readDialGauge()
        self.x_dial_setup = 'gcodes/x_dial_indicator_setup.gcode'
        self.z_dial_setup = 'gcodes/z_dial_indicator_setup.gcode'
        self.x_dial_calibration = 'gcodes/x_dial_indicator_calibration.gcode'
        self.y_dial_calibration = 'gcodes/y_dial_indicator_calibration.gcode'
        self.z_dial_calibration = 'gcodes/z_dial_indicator_calibration.gcode'
        self.syringe_pump_dial_calibration = 'gcodes/syringe_pump_dial_indicator_calibration.gcode'

    def printer_home(self, devices):
        devices.ports['printer'].write(('\r\n' + 'G28' + '\r\n').encode('utf-8'))

    def run_printer_gcode(self, devices, gcode):
        with open(gcode, 'r') as gcode:
            gcode_lines = gcode.read().splitlines()
        for line in gcode_lines:
            devices.ports['printer'].write(('\r\n' + line + '\r\n').encode('utf-8'))

    def printer_x_prep(self, devices):
        self.run_printer_gcode(devices, self.x_dial_setup)

    def printer_z_prep(self, devices):
        self.run_printer_gcode(devices, self.z_dial_setup)

    def run_accuracy_test(self, devices, gcode):
        with open(gcode, 'r') as gcode:
            gcode_lines = gcode.read().splitlines()
        reading = []
        for line in gcode_lines:
            devices.ports['printer'].write(('\r\n' + line + '\r\n').encode('utf-8'))
            read = ""
            while "ok" not in str(read):
                read = devices.ports['printer'].readline()
            sleep(4)
            reading.append(self.mt_gauge.get_dial_reading(
                           devices.ports['dialswitch']))
        return reading

    def x_axis_accuracy_test(self, devices):
        reading = self.run_accuracy_test(devices, self.x_dial_calibration)
        return reading

    def y_axis_accuracy_test(self, devices):
        reading = self.run_accuracy_test(devices, self.y_dial_calibration)
        return reading

    def z_axis_accuracy_test(self, devices):
        reading = self.run_accuracy_test(devices, self.z_dial_calibration)
        return reading

    def syringe_pump_accuracy_test(self, devices):
        reading = self.run_accuracy_test(devices, self.syringe_pump_dial_calibration)
        return reading


