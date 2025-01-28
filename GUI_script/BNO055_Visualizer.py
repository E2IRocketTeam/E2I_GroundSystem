import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from collections import deque
#

class BNO055Visualizer:
    def __init__(self, serial_port):
        self.serial_port = serial_port
        self.yaw_buffer = deque(maxlen=5)
        self.pitch_buffer = deque(maxlen=5)
        self.roll_buffer = deque(maxlen=5)

        # Define the original axes
        self.x_axis = np.array([1, 0, 0])
        self.y_axis = np.array([0, 1, 0])
        self.z_axis = np.array([0, 0, 1])

        # Setup the plot
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')

    def rotation_matrix(self, yaw, pitch, roll):
        yaw, pitch, roll = np.radians([yaw, pitch, roll])
        R_yaw = np.array([
            [np.cos(yaw), -np.sin(yaw), 0],
            [np.sin(yaw),  np.cos(yaw), 0],
            [0, 0, 1]
        ])
        R_pitch = np.array([
            [np.cos(pitch), 0, np.sin(pitch)],
            [0, 1, 0],
            [-np.sin(pitch), 0, np.cos(pitch)]
        ])
        R_roll = np.array([
            [1, 0, 0],
            [0, np.cos(roll), -np.sin(roll)],
            [0, np.sin(roll),  np.cos(roll)]
        ])
        return R_yaw @ R_pitch @ R_roll

    def smooth_data(self, buffer, value):
        buffer.append(value)
        return np.mean(buffer)

    def update(self, frame):
        try:
            while self.serial_port.in_waiting > 0:  # Only process if there's data
                line = self.serial_port.readline().decode('utf-8').strip()
                yaw_raw, pitch_raw, roll_raw = map(float, line.split(','))

                yaw = self.smooth_data(self.yaw_buffer, yaw_raw)
                pitch = self.smooth_data(self.pitch_buffer, pitch_raw)
                roll = self.smooth_data(self.roll_buffer, roll_raw)

                R = self.rotation_matrix(yaw, pitch, roll)

                x_axis_rotated = np.dot(R, self.x_axis)
                y_axis_rotated = np.dot(R, self.y_axis)
                z_axis_rotated = np.dot(R, self.z_axis)

                self.ax.cla()
                self.ax.set_xlim([-1, 1])
                self.ax.set_ylim([-1, 1])
                self.ax.set_zlim([-1, 1])
                self.ax.set_xlabel("X")
                self.ax.set_ylabel("Y")
                self.ax.set_zlabel("Z")

                self.ax.quiver(0, 0, 0, *x_axis_rotated, color='r', label='X-axis')
                self.ax.quiver(0, 0, 0, *y_axis_rotated, color='g', label='Y-axis')
                self.ax.quiver(0, 0, 0, *z_axis_rotated, color='b', label='Z-axis')

                self.ax.text2D(0.05, 0.95, f"Yaw: {yaw:.2f}°\nPitch: {pitch:.2f}°\nRoll: {roll:.2f}°", 
                               transform=self.ax.transAxes, fontsize=12, color="black")
        except Exception as e:
            print(f"Error: {e}")

    def start(self):
        self.ani = FuncAnimation(self.fig, self.update, interval=10)
        plt.show()
