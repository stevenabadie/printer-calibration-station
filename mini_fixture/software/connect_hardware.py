import serial
from serial.tools import list_ports


class connectHardware():
    def __init__(self):
        self.ports = {}

    # Need to add removal of a device from ports if it is disconnected.
    # Need to add better status and error reporting for devices already connected.

    def disconnect_all_devices(self):
        for port in self.ports:
            self.ports[port].close()
        self.ports = {}

    def connect_DFS_gauges(self):
        # X and Z 'A107MY3F'
        # Y 'A107MY3I'
        if 'dfs_y' not in self.ports or 'dfs_xz' not in self.ports and list(list_ports.grep("0403:6001")):
            for gauge in list(list_ports.grep("0403:6001")):
                port = gauge.device
                if gauge.serial_number == "A107MY3F":
                    self.ports['dfs_xz'] = serial.Serial(port, 38400)
                    if self.ports['dfs_xz'].is_open:
                        print("DFS X and Z axis force gauge connected")
                    else:
                        print("Something went wrong attempting to connect the \
                              DFS X and Z axis force gauge.")
                elif gauge.serial_number == "A107MY3I":
                    self.ports['dfs_y'] = serial.Serial(port, 38400)
                    if self.ports['dfs_y'].is_open:
                        print("DFS Y axis force gauge connected")
                    else:
                        print("Something went wrong attempting to connect the \
                              DFS Y axis force gauge.")
        else:
            print("There are no DFS force gauges connected.")

    def connect_dial_switch(self):
        if 'dialswitch' not in self.ports and list(list_ports.grep("2341:0043")):
            port = list(list_ports.grep("2341:0043"))[0].device
            self.ports['dialswitch'] = serial.Serial(port, 115200)
            if self.ports['dialswitch'].is_open:
                print("Dial Switch connected")
            else:
                print("Sorry something failed while attempting to connect.")
        else:
            print("The dial gauge switch is not connected.")
    
    def connect_actuator_controller(self):
        #Actuator USB device serial number 755303131313519152D0
        if 'actuator' not in self.ports and list(list_ports.grep("RAMBo")):
            for controller in list(list_ports.grep("RAMBo")):
                port = controller.device
                if controller.serial_number == "755303131313519152D0":
                    self.ports['actuator'] = serial.Serial(port, 250000)
                    if self.ports['actuator'].is_open:
                        print("Actuator controller connected")
                    else:
                        print("Sorry something failed while attempting to \
                              connect.")
        else:
            print("The actuator controller is not connected.")

    def connect_printer(self):
        # Need to add clear input buffer after connecting
        if 'printer' not in self.ports and list(list_ports.grep("RAMBo")):
            for controller in list(list_ports.grep("RAMBo")):
                port = controller.device
                if controller.serial_number != "755303131313519152D0":
                    self.ports['printer'] = serial.Serial(port, 250000)
                    if self.ports['printer'].is_open:
                        print("Printer controller connected")
                    else:
                        print("Sorry something failed while attempting to \
                              connect.")
                else:
                    break
        else:
            print("The printer is not connected")

    def connect_all_gauges(self):
        self.connect_DFS_gauges()
        self.connect_dial_switch()
        self.connect_actuator_controller()
        



