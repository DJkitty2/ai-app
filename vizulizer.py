import pygame
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class AudioVisualizer:
    def __init__(self):
        self.data = None
        self.samplerate = None
        self.position = 0
        self.window_size = 2048
        self.line = None
        self.fig, self.ax = plt.subplots()
        self.filename = None

    def initialize_visualizer(self, filename):
        self.filename = filename
        self.data, self.samplerate = sf.read(filename)

        if self.data.ndim > 1:  # stereo to mono
            self.data = self.data.mean(axis=1)

        self.data = self.data / np.max(np.abs(self.data))  # normalize
        self.position = 0

        pygame.mixer.init(frequency=self.samplerate)
        pygame.mixer.music.load(filename)

        # Setup matplotlib visuals
        self.fig.patch.set_facecolor('black')
        self.ax.set_facecolor('black')
        self.ax.axis('off')
        self.line, = self.ax.plot([], [], color='white', linewidth=1.2)
        self.ax.set_xlim(0, self.window_size)
        self.ax.set_ylim(-1, 1)

    def _update(self, frame):
        if self.position + self.window_size < len(self.data):
            chunk = self.data[self.position:self.position + self.window_size]
            self.line.set_ydata(chunk)
            self.line.set_xdata(np.arange(len(chunk)))
            self.position += self.window_size // 16  # smoother motion
        return self.line,

    def play_audio(self):
        if not self.filename:
            raise Exception("Visualizer not initialized. Call initialize_visualizer() first.")

        pygame.mixer.music.play()
        ani = FuncAnimation(self.fig, self._update, interval=20, blit=True)
        plt.show()

# Example usage
if __name__ == "__main__":
    visualizer = AudioVisualizer()
    visualizer.initialize_visualizer("suroke.wav")
    visualizer.play_audio()