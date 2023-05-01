from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from math import ceil

import matplotlib
matplotlib.use('Qt5Agg')

class RealTimePlotter:
    """
    A real-time 3D plotter for visualising stream data.
    """

    def __init__(self, title=None, sample_size=60, source=None, sensor_id=None, 
                 ylim=((-20,20),(-1000,1000),(-180,180)), data_file=None, marker='-', color='b'):
        self.title = title
        self.sample_size = sample_size
        self.source = source
        self.sensor_id = sensor_id
        self.ylim = ylim
        self.data_file = data_file
        self.marker = marker
        self.color = color

        self.fig = plt.figure(self.title, figsize=(12,7.5))
        self.fig.suptitle(self.title)
        self.ax = self.fig.subplots(3,3)
        self.fig.subplots_adjust(hspace=0.3, left=0.1, bottom=0.065, top=0.9)

        for i, j in np.ndindex((3, 3)):
            self.ax[i, j].grid(True)
            self.ax[i, j].set(xlabel="Time (s)", xlim=(0, self.sample_size), ylim=self.ylim[i])

        self.ax[0,0].set_title('X-axis'), self.ax[0,1].set_title('Y-axis'), self.ax[0,2].set_title('Z-axis')
        self.ax[0,0].set_ylabel('Acceleration (m/s²)'), self.ax[1,0].set_ylabel('Gyro (deg/s)'), self.ax[2,0].set_ylabel('Angle (deg)')
        self.fig.suptitle(self.title)

        self.AccX, self.AccY, self.AccZ = [np.empty(0)] * 3
        self.GyrX, self.GyrY, self.GyrZ = [np.empty(0)] * 3
        self.AngX, self.AngY, self.AngZ = [np.empty(0)] * 3

        self.line_AccX, = self.ax[0,0].plot(self.AccX, self.marker, color=self.color)
        self.line_AccY, = self.ax[0,1].plot(self.AccY, self.marker, color=self.color)
        self.line_AccZ, = self.ax[0,2].plot(self.AccZ, self.marker, color=self.color)

        self.line_GyrX, = self.ax[1,0].plot(self.GyrX, self.marker, color=self.color)
        self.line_GyrY, = self.ax[1,1].plot(self.GyrY, self.marker, color=self.color)
        self.line_GyrZ, = self.ax[1,2].plot(self.GyrZ, self.marker, color=self.color)

        self.line_AngX, = self.ax[2,0].plot(self.AngX, self.marker, color=self.color)
        self.line_AngY, = self.ax[2,1].plot(self.AngY, self.marker, color=self.color)
        self.line_AngZ, = self.ax[2,2].plot(self.AngZ, self.marker, color=self.color)

        self.line = [self.line_AccX, self.line_AccY, self.line_AccZ, 
                     self.line_GyrX, self.line_GyrY, self.line_GyrZ, 
                     self.line_AngX, self.line_AngY, self.line_AngZ]

    def animate(self, i):
        new_data = (self.source.read_data()[self.sensor_id])
        if self.data_file: self.data_file.data_save(new_data)
        Time, Acc, Gyr, Ang = float(new_data[1]), [float(x) for x in new_data[2:5]], [float(x) for x in new_data[5:8]], [float(x) for x in new_data[8:11]]

        self.AccX, self.AccY, self.AccZ = [np.append(x, (Time, Acc[i])) for i, x in enumerate([self.AccX, self.AccY, self.AccZ])]
        self.GyrX, self.GyrY, self.GyrZ = [np.append(x, (Time, Gyr[i])) for i, x in enumerate([self.GyrX, self.GyrY, self.GyrZ])]
        self.AngX, self.AngY, self.AngZ = [np.append(x, (Time, Ang[i])) for i, x in enumerate([self.AngX, self.AngY, self.AngZ])]

        data_sets = [(self.AccX, self.line_AccX), (self.AccY, self.line_AccY), (self.AccZ, self.line_AccZ),
             (self.GyrX, self.line_GyrX), (self.GyrY, self.line_GyrY), (self.GyrZ, self.line_GyrZ),
             (self.AngX, self.line_AngX), (self.AngY, self.line_AngY), (self.AngZ, self.line_AngZ)]

        for data, line in data_sets: line.set_data(data[::2], data[1::2])

        for ax in self.ax.flatten():
            if Time >= ax.get_xlim()[1] - 1:
                ax.set_xlim(ax.get_xlim()[1]-30, ax.get_xlim()[1] + self.sample_size)
                self.fig.canvas.draw_idle()

            min_data, max_data = min(ax.get_lines()[0].get_ydata()), max((ax.get_lines()[0].get_ydata()))
            if min_data < ax.get_ylim()[0] or max_data > ax.get_ylim()[1]:
                ax.set_ylim((min_data // 10) * 10, (max_data // 10 + 1) * 10)
                self.fig.canvas.draw_idle()

        return self.line

    def start(self):
        self.ani = FuncAnimation(self.fig,self.animate,interval=50,blit=True)
        return self.ani

    def on_close(self, event):
        plt.figure(self.title)
        if self.data_file:
            self.data_file.close()
            time_data = plt.gca().get_lines()[0].get_xdata()
            for ax in self.ax.flatten(): ax.set_xlim(0, ceil(time_data[-1]))
            self.fig.set_size_inches(20,12)
            plt.savefig(self.data_file.image_save(), dpi=500)
            print(f"{time_data.size} data points saved "
                  f"({time_data[-1]}s worth of data) for sensor {self.sensor_id}")
        plt.close('all')
