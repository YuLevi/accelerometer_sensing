import serial
import serial.tools.list_ports

class SerialHandler:
	def __init__(self):
		# Auto-find and select Arduino serial port
		arduino_ports = [p.device for p in serial.tools.list_ports.comports() if 'Arduino' in p.description]
		if not arduino_ports:
			raise IOError("No Arduino found")
		self.serialRead = serial.Serial(arduino_ports[0], 115200)

	def read_data(self):
		data1 = self.serialRead.readline().decode().rstrip()
		data2 = self.serialRead.readline().decode().rstrip()
		fields1, fields2 = [x.split('\t') for x in [data1, data2]]
		fields1[1], fields2[1] = [int(x)/1000 for x in [fields1[1], fields2[1]]]
		return fields1, fields2
