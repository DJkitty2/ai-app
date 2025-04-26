# chaos_shape.py

import numpy as np
import soundfile as sf
import sounddevice as sd
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
from threading import Thread
from pathlib import Path

CONFIG = {
    "file_path": "output.wav",
    "num_points": 64,
    "radius": 2.0,
    "amplitude_scale": 100,
    "min_amplitude": 0.005,  # helps ignore AI artifacts
    "chunk_size": 1024,
    "update_interval": 20,
}


def chaos_shape_visualizer():
    path = Path(CONFIG["file_path"]).resolve()
    data, fs = sf.read(path, always_2d=True)
    data = data[:, 0]  # Mono
    total_frames = len(data)
    pos = [0]  # mutable integer

    app = pg.mkQApp("Chaos Shape Visualizer")
    win = pg.GraphicsLayoutWidget(show=True)
    win.setWindowTitle("Chaos Shape")
    win.setBackground('k')
    plot = win.addPlot()
    plot.setAspectLocked(True)
    plot.hideAxis('bottom')
    plot.hideAxis('left')

    num = CONFIG["num_points"]
    angles = np.linspace(0, 2 * np.pi, num, endpoint=False)
    base_x = np.cos(angles) * CONFIG["radius"]
    base_y = np.sin(angles) * CONFIG["radius"]

    scatter = pg.ScatterPlotItem(size=4, pen=None, brush='w')
    plot.addItem(scatter)

    line_plot = pg.PlotDataItem(pen=pg.mkPen('w', width=1))  # Add a line plot to connect the dots
    plot.addItem(line_plot)

    # Initialize smoothed coordinates
    smoothed_x_coords = np.zeros(num)
    smoothed_y_coords = np.zeros(num)
    smoothing_factor = 0.2  # Adjust this value for more or less smoothing

    def update():
        nonlocal smoothed_x_coords, smoothed_y_coords
        start = pos[0]
        end = start + CONFIG["chunk_size"]
        if end >= total_frames:
            timer.stop()
            return

        segment = data[start:end]
        energy = np.abs(segment)
        energy = energy[::len(energy) // num]  # downsample to match point count

        points = []
        x_coords = []
        y_coords = []
        for i in range(num):
            amp = energy[i] if i < len(energy) else 0
            if amp < CONFIG["min_amplitude"]:
                amp = 0
            dx = base_x[i] * (1 + amp * CONFIG["amplitude_scale"] * np.random.uniform(0.9, 1.1))
            dy = base_y[i] * (1 + amp * CONFIG["amplitude_scale"] * np.random.uniform(0.9, 1.1))
            x_coords.append(dx)
            y_coords.append(dy)

        # Apply smoothing to the coordinates
        smoothed_x_coords = smoothed_x_coords * (1 - smoothing_factor) + np.array(x_coords) * smoothing_factor
        smoothed_y_coords = smoothed_y_coords * (1 - smoothing_factor) + np.array(y_coords) * smoothing_factor

        # Update points and plot
        for i in range(num):
            points.append({'pos': (smoothed_x_coords[i], smoothed_y_coords[i])})

        # Update scatter plot with smoothed points
        scatter.setData(points)

        # Update line plot with smoothed coordinates (closing the shape)
        line_plot.setData(x=smoothed_x_coords.tolist() + [smoothed_x_coords[0]],
                          y=smoothed_y_coords.tolist() + [smoothed_y_coords[0]])

    def audio_callback(outdata, frames, time, status):
        if status:
            print(status, flush=True)
        start = pos[0]
        end = start + frames
        if end >= total_frames:
            outdata[:] = 0
            raise sd.CallbackStop()
        outdata[:, 0] = data[start:end]
        pos[0] = end

    def run_audio():
        with sd.OutputStream(samplerate=fs, channels=1, callback=audio_callback,
                             blocksize=CONFIG["chunk_size"]):
            while True:
                QtCore.QCoreApplication.processEvents()

    global timer
    timer = QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(CONFIG["update_interval"])

    audio_thread = Thread(target=run_audio, daemon=True)
    audio_thread.start()

    app.exec_()

if __name__ == "__main__":
    chaos_shape_visualizer()