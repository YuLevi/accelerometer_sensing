import csv
from datetime import datetime
from serial_read import SerialHandler
from data_plotter import RealTimePlotter
from matplotlib import pyplot as plt

SENSORS_COUNT = 2
DATA_COLLECTION_ONLY = False

class SaveToFile:
    def __init__(self, filename, CSV_HEADER, save_every=10):
        self.filename = filename
        self.headers = CSV_HEADER
        self.counter = 0
        self.save_every = save_every
        self.file = open(self.filename, mode='a', newline='')
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

def live_data_plotting():
    plot_objects = {}
    date_time = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    for sensor_num in range(0, SENSORS_COUNT):
        plot_objects[sensor_num] = RealTimePlotter(title=f"Sensor {sensor_num} - {date_time}", source=data_source, 
                                                sensor_id=sensor_num, data_file=sensor_files[sensor_num])

    ani = plot_objects[0].start(), plot_objects[1].start()

    plot_objects[0].fig.canvas.mpl_connect('close_event', plot_objects[0].on_close)
    plot_objects[1].fig.canvas.mpl_connect('close_event', plot_objects[1].on_close)

    plt.show()

def data_saving():
    time_points = [[0, 0] for _ in range(SENSORS_COUNT)]

    while True:
        try:
            for sensor_num, sensor_file in enumerate(sensor_files):
                new_data = (data_source.read_data()[sensor_num])
                sensor_file.data_save(new_data)
                time_points[sensor_num][0] = float(new_data[1])
                time_points[sensor_num][1] += 1

        except Exception as e:
            print(f"Serial communication error: {str(e)}")
            for sensor_num, sensor_file in enumerate(sensor_files):
                sensor_file.close()
                print(f"{time_points[sensor_num][1]} data points saved "
                  f"({time_points[sensor_num][0]}s worth of data) for sensor {sensor_num}")
            break

# File config
timestamp_str = datetime.now().strftime("%Y-%m-%d_%H%M%S")
CSV_HEADER = ['SensorID','TimeElapsed', 'AccX', 'AccY', 'AccZ', 'GyroX', 'GyroY', 'GyroZ', 'AngleX', 'AngleY', 'AngleZ']
filenames = [f"../captured_accel_data/accel_data_{timestamp_str}_{i}.csv" for i in range(0, SENSORS_COUNT)]
sensor_files = [SaveToFile(filename, CSV_HEADER) for filename in filenames]

data_source = SerialHandler()

data_saving() if DATA_COLLECTION_ONLY else live_data_plotting()
