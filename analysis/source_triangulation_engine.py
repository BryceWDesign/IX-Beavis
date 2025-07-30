# /analysis/source_triangulation_engine.py
# Harmonic triangulation of cosmic light sources based on coherence & incidence data
# Author: Bryce Wooster

import numpy as np
from scipy.optimize import minimize

class SourceTriangulationEngine:
    """
    Triangulates the likely origin point of light sources based on:
    - Multi-angle photon trajectory data
    - Phase-coherence timestamps
    - Optical pathlength harmonics
    """

    def __init__(self, detector_positions):
        """
        detector_positions: list of (x, y, z) coordinates for light sensors
        """
        self.detectors = np.array(detector_positions)

    def compute_error(self, source_position, observed_angles):
        """
        Internal: error function based on angular mismatch
        """
        source = np.array(source_position)
        total_error = 0.0

        for i, detector in enumerate(self.detectors):
            vec = source - detector
            norm_vec = vec / np.linalg.norm(vec)

            obs_azimuth, obs_elevation = observed_angles[i]
            azimuth_vec = np.array([
                np.cos(np.radians(obs_azimuth)) * np.cos(np.radians(obs_elevation)),
                np.sin(np.radians(obs_azimuth)) * np.cos(np.radians(obs_elevation)),
                np.sin(np.radians(obs_elevation))
            ])
            angular_diff = 1 - np.dot(norm_vec, azimuth_vec)
            total_error += angular_diff**2

        return total_error

    def triangulate(self, observed_angles, initial_guess=(0, 0, 0)):
        """
        observed_angles: list of (azimuth_deg, elevation_deg) from each detector
        Returns: (x, y, z) of estimated light origin
        """
        result = minimize(
            self.compute_error,
            initial_guess,
            args=(observed_angles,),
            method='L-BFGS-B'
        )
        return result.x if result.success else None
