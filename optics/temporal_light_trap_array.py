# /optics/temporal_light_trap_array.py
# Real-world time-sliced photon persistence array
# Author: Bryce Wooster

import numpy as np
from scipy.ndimage import gaussian_filter

class TemporalLightTrapArray:
    """
    Traps high-speed light pulses using micro-lensed convergence timing,
    enabling sub-frame persistence for ultra-faint object imaging or
    time-domain separation of high-velocity photon paths.
    """

    def __init__(self, trap_grid_size=(64, 64), time_slice_ps=25):
        self.grid_x, self.grid_y = trap_grid_size
        self.time_slice_ps = time_slice_ps  # picosecond slice resolution
        self.light_field = np.zeros((self.grid_x, self.grid_y))
        self.trap_decay = np.full((self.grid_x, self.grid_y), fill_value=1.0)

    def inject_photon_event(self, x, y, intensity=1.0):
        """
        Simulates photon entry into a temporal trap cell.
        """
        if 0 <= x < self.grid_x and 0 <= y < self.grid_y:
            self.light_field[x, y] += intensity

    def decay_traps(self, decay_rate=0.985):
        """
        Applies time-based decay to simulate trapped photon persistence.
        """
        self.light_field *= decay_rate
        self.trap_decay *= decay_rate

    def enhance_trap_signal(self):
        """
        Gaussian filter applied to simulate diffracted edge glow or
        peripheral resonance for visualization + spectral drift.
        """
        return gaussian_filter(self.light_field, sigma=1.4)

    def reset_trap_array(self):
        """
        Clears all trap state (used between integration cycles).
        """
        self.light_field.fill(0)
        self.trap_decay.fill(1.0)

    def get_trapped_light_snapshot(self):
        """
        Returns the current visible state of trapped photons.
        """
        return np.copy(self.light_field)
