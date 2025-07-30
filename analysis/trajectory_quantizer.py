# /analysis/trajectory_quantizer.py
# Converts angular light data into quantized trajectories for pattern analysis
# Author: Bryce Wooster

import numpy as np

class TrajectoryQuantizer:
    """
    Quantizes angular incidence data from photonic input to enable pattern recognition
    and angular signature mapping across femto-to-nanosecond exposure ranges.
    """

    def __init__(self, angular_resolution_deg=0.05):
        """
        angular_resolution_deg: granularity of angle mapping in degrees
        """
        self.resolution = angular_resolution_deg

    def quantize_angle(self, angle_deg):
        """
        Maps a single angle to the nearest quantized value.
        """
        return round(angle_deg / self.resolution) * self.resolution

    def quantize_trajectory(self, raw_trajectory):
        """
        Accepts list of (x, y, z) photon incidence vectors.
        Returns list of quantized (azimuth_deg, elevation_deg).
        """
        quantized = []
        for vec in raw_trajectory:
            x, y, z = vec
            r = np.linalg.norm(vec)
            azimuth = np.degrees(np.arctan2(y, x)) % 360
            elevation = np.degrees(np.arcsin(z / r))
            az_q = self.quantize_angle(azimuth)
            el_q = self.quantize_angle(elevation)
            quantized.append((az_q, el_q))
        return quantized

    def build_trajectory_map(self, quantized_trajectories):
        """
        Builds a spatial occurrence matrix (histogram) of incoming trajectories.
        Returns: dict[(azimuth_deg, elevation_deg)] -> count
        """
        histogram = {}
        for az, el in quantized_trajectories:
            key = (az, el)
            histogram[key] = histogram.get(key, 0) + 1
        return histogram
