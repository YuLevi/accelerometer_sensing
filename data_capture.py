import serial
import serial.tools.list_ports
import csv
from datetime import datetime

# Auto-find and select Arduino serial port
arduino_ports = [p.device for p in serial.tools.list_ports.comports() if 'Arduino' in p.description]
if not arduino_ports:
    raise IOError("No Arduino found")

# File config
timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"../captured_accel_data/accel_data_{timestamp_str}.csv"
CSV_HEADER = ['SensorID','TimeElapsed', 'AccX', 'AccY', 'AccZ', 'GryoX', 'GryoY', 'GryoZ', 'AngleX', 'AngleY', 'AngleZ']

# Serial port configuration
with serial.Serial(arduino_ports[0], 115200) as serialRead:
    # Open CSV file for appending
    with open(filename, mode='a', newline='') as data_file:
        data_file = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data_file.writerow(CSV_HEADER)

        # Read data from serial port (with error handling)
        while True:
            try:
                # Read line from serial port, decode it and write to file
                line = serialRead.readline().decode().strip()
                values = line.split(',')
                data_file.writerow(values)

            except serial.SerialException as e:
                    print(f"Serial port disconnected: {e}")
                    break
            
            except Exception as e:
                    print(f"Error reading serial port: {e}")
