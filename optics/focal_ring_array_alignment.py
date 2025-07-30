# /optics/focal_ring_array_alignment.py
# Alignment logic for 360-degree light convergence rings
# Author: Bryce Wooster

import numpy as np

class FocalRingArrayAlignment:
    """
    Aligns concentric micromirror rings for full inward convergence of
    light at variable incident angles. Handles radial adjustment per
    ring layer to ensure phase-synchronized focus onto temporal trap.
    """

    def __init__(self, num_rings=6, ring_radius_step=2.5):
        self.num_rings = num_rings
        self.ring_radius_step = ring_radius_step  # mm per ring layer
        self.ring_offsets = np.zeros(num_rings)  # Radial phase correction offsets

    def set_ring_offset(self, ring_index, offset_value):
        """
        Sets custom micromirror offset for a specific ring.
        This compensates for curvature-induced beam divergence.
        """
        if 0 <= ring_index < self.num_rings:
            self.ring_offsets[ring_index] = offset_value

    def compute_alignment_matrix(self):
        """
        Returns a matrix describing current ring radius and offset configuration.
        Useful for mechanical mirror mounts or piezo-controlled ring arrays.
        """
        alignment_matrix = []
        for i in range(self.num_rings):
            radius = (i + 1) * self.ring_radius_step
            offset = self.ring_offsets[i]
            alignment_matrix.append({
                'ring_index': i,
                'radius_mm': radius,
                'offset_mm': offset
            })
        return alignment_matrix

    def auto_tune_offsets(self, incident_angle_deg):
        """
        Automatically adjusts each ring's offset based on angular divergence
        and a harmonic convergence model (Tesla 3-6-9 logic applied).
        """
        angle_rad = np.deg2rad(incident_angle_deg)
        for i in range(self.num_rings):
            harmonic_mod = (i % 3 + 1) * 0.369  # Tesla logic: 3, 6, 9 coefficient scaling
            self.ring_offsets[i] = np.tan(angle_rad) * (i + 1) * harmonic_mod

    def get_ring_offset(self, ring_index):
        """
        Returns the current offset for a specific ring.
        """
        if 0 <= ring_index < self.num_rings:
            return self.ring_offsets[ring_index]
        return None
