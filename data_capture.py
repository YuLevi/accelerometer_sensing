import csv
from datetime import datetime
from serial_read import SerialHandler
from data_plotter import RealTimePlotter
from matplotlib import pyplot as plt

SENSORS_COUNT = 2

class SaveToFile:
    def __init__(self, filename, CSV_HEADER, save_every=10):
        self.filename = filename
        self.headers = CSV_HEADER
        self.counter = 0
        self.save_every = save_every
        self.file = open(self.filename, mode='w', newline='')
        self.data_file = csv.writer(self.file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        self.data_file.writerow(self.headers)

    def data_save(self, collected_data):
        self.data_file.writerow(collected_data)
        self.counter += 1
        if self.counter % self.save_every == 0:
            self.file.flush()  # flush buffer to ensure data is written to disk

    def image_save(self):
        return f"{self.filename[:-3]}.png"

    def close(self):
        self.file.close()

# File config
timestamp_str = datetime.now().strftime("%Y-%m-%d_%H%M%S")
CSV_HEADER = ['SensorID','TimeElapsed', 'AccX', 'AccY', 'AccZ', 'GyroX', 'GyroY', 'GyroZ', 'AngleX', 'AngleY', 'AngleZ']
filenames = [f"../captured_accel_data/accel_data_{timestamp_str}_{i}.csv" for i in range(0, SENSORS_COUNT)]
sensor_files = [SaveToFile(filename, CSV_HEADER) for filename in filenames]

plot_objects = {}
date_time = datetime.now().strftime("%d/%m/%Y %H:%M")
data_source = SerialHandler()
for sensor_num in range(0, SENSORS_COUNT):
    plot_objects[sensor_num] = RealTimePlotter(title=f"Sensor {sensor_num} - {date_time}", source=data_source, 
                                               sensor_id=sensor_num, data_file=sensor_files[sensor_num])

ani = plot_objects[0].start(), plot_objects[1].start()

plot_objects[0].fig.canvas.mpl_connect('close_event', plot_objects[0].on_close)
plot_objects[1].fig.canvas.mpl_connect('close_event', plot_objects[1].on_close)

plt.show()
