# Class for writing/reading and parsing data with the Nextech DFS force gauge 


class nextechReading():
    def zero_gauge(self, devices, gauge):
        devices.ports[gauge].write(('z\n').encode('utf-8'))
        devices.ports[gauge].reset_output_buffer()

    def serial_read_write(self, devices, gauge, command):
        devices.ports[gauge].write((command + '\n').encode('utf-8'))
        return devices.ports[gauge].readline()

    def clean_reading(self, reading):
        reading = str(reading)
        if "b'\\r" not in reading and "b'" not in reading:
            return "Error: Value format different than expected in beginning"
        elif "b'\\r" in reading:
            reading_split = (reading.partition("b'\\r"))[2]
        elif "b'" in reading:
            reading_split = (reading.partition("b'"))[2]

        if "\\tN" not in reading_split:
            return "Error: Value format different than expected in end"
        elif "\\tN" in reading_split:
            reading_cleaned = reading_split[:reading_split.find("\\tN")]

        return reading_cleaned

    def get_clean_force_reading(self, devices, gauge, command):
        reading = self.serial_read_write(devices, gauge, command)
        return self.clean_reading(reading)
