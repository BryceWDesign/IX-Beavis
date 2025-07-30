# /sensors/deep_field_sensor_array.py
# Constructs and manages ultra-long exposure photon detection array
# Author: Bryce Wooster

import numpy as np

class DeepFieldSensorArray:
    """
    Emulates a deep-field photon accumulation sensor matrix with noise reduction.
    Useful for collecting faint interstellar light over long exposures.
    """

    def __init__(self, width=128, height=128, integration_time_s=600.0):
        self.width = width
        self.height = height
        self.integration_time_s = integration_time_s
        self.signal_matrix = np.zeros((height, width), dtype=np.float64)
        self.noise_profile = self._generate_noise_profile()

    def _generate_noise_profile(self):
        """
        Simulates thermal and sensor-line noise typical of long exposure
        imaging arrays (CCD or superconducting nanowire types).
        """
        thermal_noise = np.random.normal(loc=0.0, scale=0.002, size=(self.height, self.width))
        line_noise = np.random.normal(loc=0.0, scale=0.001, size=(self.height, 1))
        return thermal_noise + line_noise

    def accumulate_photons(self, photon_events):
        """
        Integrates incident photon events into the signal matrix, mimicking deep
        space long-term light collection from micro-mirror field convergence.
        """
        for (x, y, intensity) in photon_events:
            if 0 <= x < self.width and 0 <= y < self.height:
                self.signal_matrix[y, x] += intensity

    def finalize_image(self):
        """
        Outputs the final image matrix after integrating all photons,
        subtracting the estimated noise floor.
        """
        cleaned_image = self.signal_matrix - self.noise_profile
        cleaned_image[cleaned_image < 0] = 0
        return cleaned_image

    def reset(self):
        """
        Clears the signal matrix for a fresh observation window.
        """
        self.signal_matrix = np.zeros((self.height, self.width), dtype=np.float64)
