# /optics/temporal_lens_matrix.py
# Temporal lensing matrix for photon phase-delay imaging
# Author: Bryce Wooster

import numpy as np

class TemporalLensMatrix:
    """
    A phased-lens grid system designed to slow, track, and imprint photons over
    nanosecond-scale durations using electro-optical phase delay elements. Real-world
    build basis includes integrated Pockels cells and high-speed refractive lenses.
    """

    def __init__(self, grid_size=(5, 5), delay_range_ns=(0.1, 10.0)):
        self.grid_size = grid_size
        self.delay_range_ns = delay_range_ns
        self.phase_grid = self._initialize_phase_matrix()

    def _initialize_phase_matrix(self):
        """
        Initializes a 2D array of phase delay elements with tunable values.
        """
        rows, cols = self.grid_size
        min_delay, max_delay = self.delay_range_ns
        return np.random.uniform(min_delay, max_delay, size=(rows, cols))

    def apply_phase_delays(self, incoming_wavefront):
        """
        Applies phase delays to an incoming 2D wavefront matrix.
        """
        if incoming_wavefront.shape != self.phase_grid.shape:
            raise ValueError("Wavefront shape must match temporal lens matrix.")

        delayed_wavefront = incoming_wavefront * np.exp(
            1j * 2 * np.pi * self.phase_grid / 1e3  # scale nanoseconds to THz cycles
        )
        return delayed_wavefront

    def update_phase_element(self, row, col, new_delay_ns):
        """
        Allows for real-time tuning of any lens matrix element (e.g., via voltage control).
        """
        if 0 <= row < self.grid_size[0] and 0 <= col < self.grid_size[1]:
            self.phase_grid[row][col] = np.clip(
                new_delay_ns, self.delay_range_ns[0], self.delay_range_ns[1]
            )

    def get_matrix_state(self):
        """
        Returns current delay values for diagnostics.
        """
        return self.phase_grid.copy()
