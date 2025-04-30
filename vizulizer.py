# chaos_shape_pretty.py

import numpy as np
import soundfile as sf
import sounddevice as sd
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
from threading import Thread
from pathlib import Path

# Configuration
CONFIG = {
    "file_path": "suroke.wav",
    "num_points": 500,
    "radius": 2.0,
    "amplitude_scale": 80,
    "min_amplitude": 0.005,
    "chunk_size": 1024,
    "update_interval": 16,  # slightly faster updates (~60 FPS)
}

def chaos_shape_visualizer():
    # Load audio
    path = Path(CONFIG["file_path"]).resolve()
    data, sample_rate = sf.read(path, always_2d=True)
    data = data[:, 0]  # Use mono
    total_frames = len(data)
    pos = [0]  # Mutable position

    # Set up window
    app = pg.mkQApp("vizulizer")
    win = pg.GraphicsLayoutWidget(show=True)
    win.setWindowTitle("vizulizer")
    win.setBackground('#0b0c1e')  # Deep navy background

    plot = win.addPlot()
    plot.setAspectLocked(True)
    plot.hideAxis('bottom')
    plot.hideAxis('left')

    # Create base shape
    num_points = CONFIG["num_points"]
    angles = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
    base_x = np.cos(angles)
    base_y = np.sin(angles)

    scatter = pg.ScatterPlotItem(size=6, pen=pg.mkPen(None), brush=pg.mkBrush(255, 255, 255, 150))  # soft white
    plot.addItem(scatter)

    line_plot = pg.PlotDataItem(pen=pg.mkPen(color=(255, 150, 255, 150), width=2))
    plot.addItem(line_plot)

    # Smooth movement
    smoothed_x = np.zeros(num_points)
    smoothed_y = np.zeros(num_points)
    smoothing_factor = 0.15

    # Color shifting
    hue = [0]  # mutable hue

    def update():
        nonlocal smoothed_x, smoothed_y

        start, end = pos[0], pos[0] + CONFIG["chunk_size"]
        if end >= total_frames:
            timer.stop()
            return

        segment = data[start:end]
        energy = np.abs(segment)
        energy = energy[::len(energy) // num_points]  # downsample

        # Breathing effect
        breathe = 1.0 + 0.05 * np.sin(QtCore.QTime.currentTime().msec() / 1000 * np.pi * 2)

        x_coords = []
        y_coords = []

        for i in range(num_points):
            amp = energy[i] if i < len(energy) else 0
            amp = amp if amp >= CONFIG["min_amplitude"] else 0
            stretch = (1 + amp * CONFIG["amplitude_scale"] * np.random.uniform(0.95, 1.05))
            dx = base_x[i] * CONFIG["radius"] * stretch * breathe
            dy = base_y[i] * CONFIG["radius"] * stretch * breathe
            x_coords.append(dx)
            y_coords.append(dy)

        # Smooth movement
        smoothed_x = smoothed_x * (1 - smoothing_factor) + np.array(x_coords) * smoothing_factor
        smoothed_y = smoothed_y * (1 - smoothing_factor) + np.array(y_coords) * smoothing_factor

        # Update scatter
        scatter.setData([{'pos': (smoothed_x[i], smoothed_y[i])} for i in range(num_points)])

        # Update line (closed loop)
        line_plot.setData(
            x=np.append(smoothed_x, smoothed_x[0]),
            y=np.append(smoothed_y, smoothed_y[0])
        )

        # Shift line color over time
        hue[0] = (hue[0] + 0.2) % 360
        color = pg.QtGui.QColor()
        color.setHsv(int(hue[0]), 255, 255, 150)
        line_plot.setPen(pg.mkPen(color=color, width=2))

    def audio_callback(outdata, frames, time, status):
        if status:
            print("Audio callback status:", status, flush=True)
        start, end = pos[0], pos[0] + frames
        if end >= total_frames:
            outdata[:] = 0
            raise sd.CallbackStop()
        outdata[:, 0] = data[start:end]
        pos[0] = end

    def run_audio():
        with sd.OutputStream(
            samplerate=sample_rate,
            channels=1,
            callback=audio_callback,
            blocksize=CONFIG["chunk_size"]
        ):
            while True:
                QtCore.QCoreApplication.processEvents()

    # Timer
    global timer
    timer = QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(CONFIG["update_interval"])

    # Start audio thread
    audio_thread = Thread(target=run_audio, daemon=True)
    audio_thread.start()

    app.exec_()

if __name__ == "__main__":
    chaos_shape_visualizer()
