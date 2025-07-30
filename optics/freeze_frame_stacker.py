# /optics/freeze_frame_stacker.py
# High-resolution photon frame stacker with micro-temporal freeze logic
# Author: Bryce Wooster

import numpy as np

class FreezeFrameStacker:
    """
    Captures and accumulates freeze-frames of light signals
    based on harmonic coherence windows and photon phase shifts.
    Enables layer-by-layer photonic 'time slicing'.
    """

    def __init__(self, frame_resolution=1e-12, max_frames=5000):
        """
        frame_resolution: minimum frame separation (in seconds)
        max_frames: max number of time-stacked photon captures
        """
        self.frame_resolution = frame_resolution
        self.max_frames = max_frames
        self.frames = []

    def capture_frame(self, light_data, timestamp):
        """
        Stores light sample only if it fits temporal criteria.
        light_data: np.array of light intensities/spectral vectors
        timestamp: time (in seconds) of photon arrival
        """
        if not self.frames or abs(timestamp - self.frames[-1]['timestamp']) >= self.frame_resolution:
            if len(self.frames) < self.max_frames:
                self.frames.append({
                    'timestamp': timestamp,
                    'data': light_data.copy()
                })

    def get_stack(self):
        """
        Returns list of stacked freeze-frames
        """
        return self.frames

    def clear(self):
        self.frames = []
