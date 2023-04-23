import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from datetime import datetime

class RealTimePlotter:
    """
    A real-time 3D plotter for visualising stream data.
    """

    def __init__(self, title=None, xlim=(-10, 10), ylim=(-10, 10), zlim=(-10, 10), marker='o-', color='b'):
        """
        Create a new RealTimePlotter object.

        Args:
        - title: str, the title of the plot (default: None)
        - xlim: tuple or list of length 2, the limits of the x-axis (default: (-10, 10))
        - ylim: tuple or list of length 2, the limits of the y-axis (default: (-10, 10))
        - zlim: tuple or list of length 2, the limits of the z-axis (default: (-10, 10))
        - marker: str, the style of the data markers (default: 'o-')
        - color: str, the color of the data line (default: 'b')
        """
        self.fig = plt.figure(title, figsize=(6,4))
        self.ax = self.fig.subplots(3,1)
        self.fig.subplots_adjust(hspace=0.3)
        for ax in self.ax: 
            ax.grid(True)
            ax.set_xlabel("Time (s)")
            ax.set_xlim(0,60)
        self.ax[0].set_ylabel("X-axis"), self.ax[1].set_ylabel("Y-axis"), self.ax[2].set_ylabel("Z-axis")
        self.ax[0].set_ylim(*xlim), self.ax[1].set_ylim(*ylim), self.ax[2].set_ylim(*zlim)
        self.fig.suptitle(title)
        self.x, self.y, self.z = [], [], []
        self.line_x, = self.ax[0].plot(self.x, marker, color=color)
        self.line_y, = self.ax[1].plot(self.y, marker, color=color)
        self.line_z, = self.ax[2].plot(self.z, marker, color=color) 

    def update_plot(self, elapsed_time, new_data):
        x, y, z = new_data
        self.x.append((elapsed_time, x)), self.y.append((elapsed_time, y)), self.z.append((elapsed_time, z))
        self.line_x.set_data(*zip(*self.x))
        self.line_y.set_data(*zip(*self.y))
        self.line_z.set_data(*zip(*self.z))

        for ax, data in zip(self.ax, [self.x, self.y, self.z]):
            if elapsed_time >= ax.get_xlim()[1] - 1:
                ax.set_xlim(ax.get_xlim()[0], 2*ax.get_xlim()[1])
                ax.figure.canvas.draw()
            min_data, max_data = min(d[1] for d in data), max(d[1] for d in data)
            data_range = np.ptp([d[1] for d in data])
            if not data_range: data_range = 1  # Avoid zero range
            ax.set_ylim(min_data - 0.1 * data_range, max_data + 0.1 * data_range)
        plt.pause(0.01)

    def __enter__(self):
        plt.ion()
        plt.show()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        plt.savefig(f"../captured_accel_data/realtime_plot_{timestamp_str}.png")    
        plt.show(block=True)
        plt.close()
